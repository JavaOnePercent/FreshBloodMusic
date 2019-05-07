import re
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import auth
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.views import APIView

from .models import *
from django.http import HttpResponse, Http404
from .uploader import save_album, save_performer, save_track, save_playlist
from .serializers import *
from .model_methods import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics

from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ParseError


@ensure_csrf_cookie
def get_token(request):
    return HttpResponse(status=status.HTTP_200_OK)


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


def get_performer(request):
    user_id = auth.get_user(request).id
    try:
        performer = Performer.objects.get(user_id=user_id)
    except Performer.DoesNotExist:
        raise ParseError('User must be logged in to access this method')
    return performer


class PostLimitOffsetPagination(PageNumberPagination):
    page_size = 12


class TrackOverview(generics.ListCreateAPIView):
    serializer_class = NoLinkTrackSerializer
    pagination_class = PostLimitOffsetPagination

    def create(self, request, *args, **kwargs):
        album = request.POST["album"]
        audio = request.FILES["track"]
        name = request.POST["track_name"]
        track = save_track(album, name, audio, get_performer(request))
        return Response({"index": request.POST["index"], 'id': track.id}, status=status.HTTP_201_CREATED)

    def handle_exception(self, exc):
        if type(exc) == ParseError:
            return Response(exc.args[0], status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        try:
            filter = self.request.query_params['filter']
        except MultiValueDictKeyError:
            raise ParseError('Filter param must be set')

        if filter != 'popular':
            TrackOverview.serializer_class = NoLinkTrackSerializer
            TrackOverview.pagination_class = PostLimitOffsetPagination

            request = self.request

            if filter == 'favorite':
                likedtracks = LikedTrack.objects.filter(user_id=auth.get_user(request).id).values_list('trc_id').order_by('id')
                ordering = 'FIELD(id, %s)' % ','.join(str(id) for id in likedtracks[0])
                tracks = Track.objects.filter(id__in=likedtracks).extra(
                    select={'ordering': ordering}, order_by=('ordering',))
            elif filter == 'recommended':
                identracks = TrackRecommendation.get_recommendation(auth.get_user(request).id)
                ordering = 'FIELD(id, %s)' % ','.join(str(id) for id in identracks)
                tracks = Track.objects.filter(pk__in=identracks).extra(
                    select={'ordering': ordering}, order_by=('ordering',))
            elif filter == 'genre':
                try:
                    genre = self.request.query_params['genre']
                except MultiValueDictKeyError:
                    raise ParseError('Filter by genre must have genre param')
                tracks = Track.objects.select_related('alb_id__stl_id__gnr_id').filter(alb_id__stl_id__gnr_id=genre)

            elif filter == 'style':
                try:
                    style = self.request.query_params['style']
                except MultiValueDictKeyError:
                    raise ParseError('Filter by style must have style param')
                tracks = Track.objects.select_related('alb_id__stl_id').filter(alb_id__stl_id=style)

            elif filter == 'all':
                tracks = Track.objects.select_related('alb_id__stl_id__gnr_id').all()
            else:
                raise ParseError('Filter value is incorrect')

            if filter != 'recommended' and filter != 'favorite':
                try:
                    sort = self.request.query_params['sort']
                except MultiValueDictKeyError:
                    sort = 'popularity'
                if sort == 'popularity':
                    tracks = tracks.order_by('-rating_trc')
                elif sort == 'time':
                    tracks = tracks.order_by('-date_trc')
            return tracks

        else:
            try:
                limit = self.request.query_params['limit']
                interval = self.request.query_params['interval']
            except MultiValueDictKeyError:
                raise ParseError('Filter by popularity requires limit and interval params')
            TrackOverview.serializer_class = TopTrackSerializer
            TrackOverview.pagination_class = None
            tracks = Track.objects.order_by('-rating_trc').filter(
                date_trc__gte=date.today() - timedelta(days=int(interval)))[:int(limit)]
            return tracks


class TrackDetail(APIView):
    def get_next(self, user):
        try:
            if user is not None:
                recommendations = TrackRecommendation.get_recommendation(user)
                if len(recommendations) != 0:
                    track = Track.objects.get(id=recommendations[0])
                else:
                    track = Track.objects.get(id=1)

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
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        delete = TrackMethods.delete(pk, auth.get_user(request).id)
        if delete:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AlbumsList(APIView):

    def get(self, request, format=None):
        try:
            sort = request.query_params['sort']
        except MultiValueDictKeyError:
            sort = 'new'
        try:
            performer = request.query_params['performer']
            albums = Album.objects.filter(per_id=performer)
        except MultiValueDictKeyError:
            albums = Album.objects.all()

        if sort == 'new':
            albums = albums.order_by('-date_alb')
        elif sort == 'popular':
            albums = Album.objects.all().order_by('-rating_alb')
        else:
            return Response('Incorrect sort key value', status=status.HTTP_400_BAD_REQUEST)
        ser = AlbumSerializer(albums, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def post(self, request):
        album_name = request.POST["name"]
        gen_id = request.POST["gen_id"]
        description = request.POST["description"]
        try:
            photo = request.FILES["photo"]
        except MultiValueDictKeyError:
            photo = None
        album = save_album(performer=get_performer(request), name=album_name, genre=gen_id, logo=photo,
                           description=description)
        return Response({"alb_id": album.id}, status=status.HTTP_201_CREATED)


class AlbumDetail(APIView):

    def get(self, request, pk):
        try:
            albums = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            return Response('Wrong album id', status=status.HTTP_400_BAD_REQUEST)
        ser = AlbumTracksSerializer(albums)
        return Response(ser.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        delete = AlbumMethods.delete(pk, auth.get_user(request).id)
        if delete:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PlaylistsList(APIView):

    def get(self, request, format=None):
        try:
            sort = request.query_params['sort']
        except MultiValueDictKeyError:
            sort = 'new'
        try:
            performer = request.query_params['performer']
            albums = Album.objects.filter(per_id=performer)
        except MultiValueDictKeyError:
            albums = Album.objects.all()

        if sort == 'new':
            albums = albums.order_by('-date_alb')
        elif sort == 'popular':
            albums = Album.objects.all().order_by('-rating_alb')
        else:
            return Response('Incorrect sort key value', status=status.HTTP_400_BAD_REQUEST)
        ser = AlbumSerializer(albums, many=True)
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        title = request.POST["title"]
        try:
            image = request.FILES["image"]
        except MultiValueDictKeyError:
            image = None
        save_playlist(auth.get_user(request), title, image)
        return Response(status=status.HTTP_201_CREATED)


class PlaylistDetail(APIView):

    def get(self, request, pk):
        try:
            albums = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            return Response('Wrong album id', status=status.HTTP_400_BAD_REQUEST)
        ser = AlbumTracksSerializer(albums)
        return Response(ser.data, status=status.HTTP_200_OK)

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
        try:
            limit = request.query_params['limit']
        except MultiValueDictKeyError:
            limit = 5
        performer = Performer.objects.order_by('-rating_per')[:int(limit)]
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
            '''for album in serializer.data["albums"]:
                for track in album["tracks"]:
                    track["likes"] = LikedTrackMethods.likesAmount(track["id"])'''
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
        save_performer(pk, name, label, description, get_performer(request))

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
        performer = get_performer(request)
        return Response({'username': auth.get_user(request).username, 'per_id': performer.id}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            performer = get_performer(request)
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
        User.objects.create_user(username, '1@1.ru', password).save()
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        performer = PerformerMethods.create(auth.get_user(request).id, username, '')
        return Response({'username': auth.get_user(request).username, 'per_id': performer.id}, status=status.HTTP_200_OK)
