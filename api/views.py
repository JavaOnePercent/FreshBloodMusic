import re
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import auth
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.views import APIView

from .models import Performer, Genre, GenreStyle, Album, Track, LikedTrack, TrackHistory
from django.db.models import Q
from django.http import HttpResponse, Http404
from .uploader import Compressor, save_album, save_performer
from .serializers import TrackSerializer, NoLinkTrackSerializer, GenreSerializer, GenreStyleSerializer, \
    PerformerSerializer, TopTrackSerializer, FullPerformerSerializer, AlbumSerializer, LikedTrackSerializer, \
    TrackHistorySerializer
from .model_methods import TrackMethods, LikedTrackMethods, GenreMethods, GenreStyleMethods, PerformerMethods, \
    AlbumMethods, TrackHistoryMethods, TrackRecommendation, TrackReportMethods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
import math
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    CursorPagination,
    )

from pprint import pprint



from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf


@ensure_csrf_cookie
def get_token(request):
    return HttpResponse(status=status.HTTP_200_OK)


def main_view(request):  # главная
    file = open('./mainapp/static/mainapp/index.html', 'r')
    index = file.read()
    file.close()
    return HttpResponse(index, content_type="text/html")
    # return render(request, 'mainapp/homePage.html', {'username': auth.get_user(request).username, 'genre': Genre.objects.all()})


'''@api_view(['GET'])  # запрос следующего трека
def next_track(request):
    if request.method == 'GET':
        tracks = TrackMethods.get_two(request.query_params)
        is_liked = LikedTrackMethods.check_if_liked(auth.get_user(request).id, tracks[0].id)
        serializer = TrackSerializer(tracks, many=True)
        serializer.data[0]["is_liked"] = is_liked
        return Response({'current': serializer.data[0], 'next': serializer.data[1]}, status=status.HTTP_200_OK)'''


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


class TrackOverview(generics.ListAPIView):
    serializer_class = NoLinkTrackSerializer
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self):
        gen = self.request.query_params['gen']
        sty = self.request.query_params['sty']
        bool = self.request.query_params['bool']
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
                if bool == 'popular':
                    tracks = tracks.order_by('-rating_trc')
                elif bool == 'time':
                    tracks = tracks.order_by('-date_trc')
            return tracks
        elif sty != '' and gen == '':
            tracks = Track.objects.select_related('alb_id__stl_id').filter(alb_id__stl_id=sty)
            if bool == 'popular':
                tracks = tracks.order_by('-rating_trc')
            elif bool == 'time':
                tracks = tracks.order_by('-date_trc')
            return tracks


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
            serializer = TrackSerializer(track)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif pk == 'next':
            track = self.get_next(auth.get_user(request).id)
            serializer = TrackSerializer(track)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


'''def gettrack(authuser):  # для Димы
    tracks = Track.objects.all().filter(id=TrackRecommendation.get_recommendation(authuser)[0])
    return tracks'''


@api_view(['GET'])
def top(request):
    if request.method == "GET":
        #per = request.query_params['per']
        #if per == 'month':
        month = Track.objects.order_by('rating_trc').reverse().filter(date_trc__gte=date.today() - timedelta(days=31))[:1]
        #elif per == 'week':
        week = Track.objects.order_by('rating_trc').reverse().filter(date_trc__gte=date.today() - timedelta(days=7))[:1]
        month = month.union(week)
        monthS = TopTrackSerializer(month, many=True)
        data = {}
        try:
            data['month'] = monthS.data[0]
        except IndexError:
            data['month'] = None
        try:
            data['week'] = monthS.data[1]
        except IndexError:
            data['week'] = None
        return Response(data, status=status.HTTP_200_OK)


class Names:
    name_track = ""
    image_track = ""

    def __init__(self, name_track, image_track):
        self.name_track = name_track
        self.image_track = image_track


@api_view(['POST', 'GET'])
def albums(request):  # нужно сделать отдельный запрос для каждого трека, и тогда можно будет отслеживать процесс их загрузки
    if request.method == 'POST':
        album_name = request.POST["name"]
        gen_id = request.POST["gen_id"]
        try:
            photo = request.FILES["photo"]
        except MultiValueDictKeyError:
            photo = None
        tracks = request.FILES.getlist('track')
        track_name = request.POST.getlist("track_name")
        pprint(track_name)
        print(request.POST)
        save_album(user=auth.get_user(request).id, name=album_name, genre=gen_id, logo=photo, tracks=tracks, track_name=list(track_name))

        return HttpResponse(status=200)

    if request.method == "GET":
        albums = AlbumMethods.get(auth.get_user(request).id)
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    '''def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)'''


'''@api_view(['PUT', 'POST', 'GET'])
def performers(request):
    if request.method == 'POST' or request.method == 'PUT':  # создание или изменение исполнителя
        name = request.POST["name"]
        try:
            label = request.FILES["label"]
        except MultiValueDictKeyError:
            label = None
        description = request.POST["description"]
        id = request.POST["id"]
        save_performer(id, auth.get_user(request).id, name, label, description)
        return Response(status=status.HTTP_200_OK)
    if request.method == "GET":  # получение исполнителя по пользователю
        user = auth.get_user(request).id
        performer = PerformerMethods.get(user)
        serializer = FullPerformerSerializer(performer)
        return Response(serializer.data, status=status.HTTP_200_OK)'''


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


@api_view(['GET'])
def report(request):
    if request.method == 'GET':
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
