import re
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import auth
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.views import APIView

from .models import Performer, Genre, GenreStyle, Album, Track, LikedTrack, TrackHistory
from django.http import HttpResponse, Http404
from .uploader import save_album, save_performer, save_track
from .serializers import TrackSerializer, NoLinkTrackSerializer, GenreSerializer, GenreStyleSerializer, \
    PerformerSerializer, TopTrackSerializer, FullPerformerSerializer, AlbumSerializer, LikedTrackSerializer, \
    TrackHistorySerializer
from .model_methods import TrackMethods, LikedTrackMethods, GenreMethods, GenreStyleMethods, PerformerMethods, \
    AlbumMethods, TrackHistoryMethods, TrackRecommendation, TrackReportMethods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics

from rest_framework.pagination import PageNumberPagination


from pprint import pprint


@ensure_csrf_cookie
def get_token(request):
    return HttpResponse(status=status.HTTP_200_OK)


def main_view(request):  # главная
    file = open('./mainapp/static/mainapp/index.html', 'r')
    index = file.read()
    file.close()
    return HttpResponse(index, content_type="text/html")
    # return render(request, 'mainapp/homePage.html', {'username': auth.get_user(request).username, 'genre': Genre.objects.all()})


@api_view(['PUT', 'DELETE', 'GET'])  # обработчик лайков
def likes(request):
    if request.method == 'PUT':  # добавление лайка
        result = LikedTrackMethods.add_like(request.query_params['track_id'], auth.get_user(request).id)
        counter = LikedTrackMethods.add_increment(request.query_params['track_id'])
        if result and counter:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':  # удаление лайка
        result = LikedTrackMethods.remove_like(request.query_params['track_id'], auth.get_user(request).id)
        counter = LikedTrackMethods.add_decrement(request.query_params['track_id'])
        if result and counter:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "GET":  # получение лайков для исполнителя
        performer = request.query_params['performer']
        likes = LikedTrackMethods.get(performer)
        serializer = LikedTrackSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostLimitOffsetPagination(PageNumberPagination):
    page_size = 12


class TrackOverview(generics.ListCreateAPIView):
    serializer_class = NoLinkTrackSerializer
    pagination_class = PostLimitOffsetPagination

    def create(self, request, *args, **kwargs):
        album = request.POST["album"]
        audio = request.FILES["track"]
        name = request.POST["track_name"]
        track = save_track(album, name, audio)
        return Response({"index": request.POST["index"], 'id': track.id}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        gen = self.request.query_params['gen']
        if gen != 'top':
            TrackOverview.serializer_class = NoLinkTrackSerializer
            TrackOverview.pagination_class = PostLimitOffsetPagination
            sty = self.request.query_params['sty']
            sort = self.request.query_params['sort']
            request = self.request
            if gen != '' and sty == '':
                if gen == 'fav':
                    likedtracks = LikedTrack.objects.filter(user_id=auth.get_user(request).id).values_list('trc_id').order_by('id')
                    ordering = 'FIELD(id, %s)' % ','.join(str(id) for id in likedtracks[0])
                    tracks = Track.objects.filter(id__in=likedtracks).extra(
                        select={'ordering': ordering}, order_by=('ordering',))
                    '''tracks = []
                    for track in likedtracks:
                        trc = Track.objects.all().get(id=track[0])
                        tracks.append(trc)'''
                elif gen == 'rec':
                    identracks = TrackRecommendation.get_recommendation(auth.get_user(request).id)
                    ordering = 'FIELD(id, %s)' % ','.join(str(id) for id in identracks)
                    tracks = Track.objects.filter(pk__in=identracks).extra(
                        select={'ordering': ordering}, order_by=('ordering',))
                elif gen != 'all':
                    tracks = Track.objects.select_related('alb_id__stl_id__gnr_id').filter(alb_id__stl_id__gnr_id=gen)
                else:
                    tracks = Track.objects.select_related('alb_id__stl_id__gnr_id').all()
                if gen != 'rec' and gen != 'fav':
                    if sort == 'popular':
                        tracks = tracks.order_by('-rating_trc')
                    elif sort == 'time':
                        tracks = tracks.order_by('-date_trc')
                return tracks
            elif sty != '' and gen == '':
                tracks = Track.objects.select_related('alb_id__stl_id').filter(alb_id__stl_id=sty)
                if sort == 'popular':
                    tracks = tracks.order_by('-rating_trc')
                elif sort == 'time':
                    tracks = tracks.order_by('-date_trc')
                return tracks
        else:
            TrackOverview.serializer_class = TopTrackSerializer
            TrackOverview.pagination_class = None
            month = Track.objects.order_by('rating_trc').reverse().filter(
                date_trc__gte=date.today() - timedelta(days=31))[:1]
            # elif per == 'week':
            week = Track.objects.order_by('rating_trc').reverse().filter(
                date_trc__gte=date.today() - timedelta(days=7))[:1]
            month = month.union(week)
            return month


class TrackDetail(APIView):
    def get_next(self, user):
        try:
            if user is not None:
                track = Track.objects.get(id=TrackRecommendation.get_recommendation(user)[0])
            else:
                track = Track.objects.filter(id__in=TrackRecommendation.get_recommendation(user)).order_by('?')[0]
            # TrackHistoryMethods.create(track.id, user)
            return track
        except Track.DoesNotExist:
            raise Http404

    def get_object(self, pk):
        try:
            return Track.objects.get(pk=pk)
        except Track.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if re.fullmatch(r'[0-9]+', pk):
            track = self.get_object(pk)
        elif pk == 'next':
            track = self.get_next(auth.get_user(request).id)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TrackSerializer(track)
        is_liked = LikedTrackMethods.check_if_liked(auth.get_user(request).id, track.id)
        data = dict(serializer.data)
        data["is_liked"] = is_liked
        #serializer.data["is_liked"] = is_liked
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        delete = TrackMethods.delete(pk, auth.get_user(request).id)
        if delete:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AlbumsList(APIView):

    def post(self, request, format=None):
        album_name = request.POST["name"]
        gen_id = request.POST["gen_id"]
        try:
            photo = request.FILES["photo"]
        except MultiValueDictKeyError:
            photo = None
        # tracks = request.FILES.getlist('track')
        # track_name = request.POST.getlist("track_name")
        # save_album(user=auth.get_user(request).id, name=album_name, genre=gen_id, logo=photo, tracks=tracks,
        # track_name=list(track_name))
        album = save_album(user=auth.get_user(request).id, name=album_name, genre=gen_id, logo=photo)
        return Response({"alb_id": album.id}, status=status.HTTP_201_CREATED)


class AlbumDetail(APIView):

    def delete(self, request, pk, format=None):
        delete = AlbumMethods.delete(pk, auth.get_user(request).id)
        if delete:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def genre(request):
    if request.method == "GET":
        try:
            gen_id = request.query_params['id']
        except MultiValueDictKeyError:
            gen_id = None
        if gen_id is None or gen_id == '':
            genres = GenreMethods.get()
            serializer = GenreSerializer(genres, many=True)
        else:
            styles = GenreStyleMethods.get(gen_id)
            serializer = GenreStyleSerializer(styles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PerformersList(APIView):

    def get(self, request, format=None):
        performer = Performer.objects.order_by('rating_per').reverse()[:3]
        serializer = PerformerSerializer(performer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PerformerDetail(APIView):
    def get_object(self, pk):
        try:
            return Performer.objects.get(pk=pk)
        except Performer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if re.fullmatch(r'[0-9]+', pk):
            performer = self.get_object(pk)
            serializer = FullPerformerSerializer(performer)
            for album in serializer.data["albums"]:
                for track in album["tracks"]:
                    track["likes"] = LikedTrackMethods.likesAmount(track["id"])
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):  # изменение исполнителя
        name = request.POST["name"]
        try:
            label = request.FILES["label"]
        except MultiValueDictKeyError:
            label = None
        description = request.POST["description"]
        save_performer(pk, name, label, description)

        return Response(status=status.HTTP_200_OK)


@api_view(['PUT', 'GET'])
def history(request):
    if request.method == 'PUT':
        result = TrackHistoryMethods.create(request.query_params['track_id'], auth.get_user(request).id)
        if result:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        tracks = TrackHistoryMethods.get(auth.get_user(request).id)
        serializer = TrackHistorySerializer(tracks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def report(request):
    if request.method == 'PUT':
        track = request.query_params['track']
        result = TrackReportMethods.create(track, auth.get_user(request).id)
        if result:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def login(request):
    if request.method == 'GET':
        performer = PerformerMethods.get(auth.get_user(request).id)
        return Response({'username': auth.get_user(request).username, 'per_id': performer.id}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            performer = PerformerMethods.get(auth.get_user(request).id)
            return Response({'username': auth.get_user(request).username, 'per_id': performer.id}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def logout(request):
    auth.logout(request)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        newuser = User.objects.create_user(username, '1@1.ru', password).save()
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        performer = PerformerMethods.create(auth.get_user(request).id, username, '')
        return Response({'username': auth.get_user(request).username, 'per_id': performer.id}, status=status.HTTP_200_OK)
