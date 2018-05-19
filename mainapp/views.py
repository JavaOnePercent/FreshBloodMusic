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
    PerformerSerializer, TopTrackSerializer, FullPerformerSerializer, AlbumSerializer, LikedTrackSerializer
from .model_methods import TrackMethods, LikedTrackMethods, GenreMethods, GenreStyleMethods, PerformerMethods, \
    AlbumMethods, TrackHistoryMethods
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


@api_view(['GET'])  # запрос следующего трека
def next_track(request):
    if request.method == 'GET':
        tracks = TrackMethods.get_two(request.query_params)
        is_liked = LikedTrackMethods.check_if_liked(auth.get_user(request).id, tracks[0].id)
        serializer = TrackSerializer(tracks, many=True)
        serializer.data[0]["is_liked"] = is_liked
        return Response({'current': serializer.data[0], 'next': serializer.data[1]}, status=status.HTTP_200_OK)


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

    elif request.method == "GET":  # получение лайков для пользователя
        likes = LikedTrackMethods.get(auth.get_user(request).id)
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
                likedtracks = LikedTrack.objects.filter(user_id=auth.get_user(request).id).values_list('trc_id')
                tracks = Track.objects.filter(id__in=likedtracks)
                '''tracks = []
                for track in likedtracks:
                    trc = Track.objects.all().get(id=track[0])
                    tracks.append(trc)'''
            elif gen == 'rec':
                likedtracks = LikedTrack.objects.all().filter(user_id=auth.get_user(request).id).values_list('trc_id')
                historytracks = TrackHistory.objects.all().filter(user_id=auth.get_user(request).id).values_list('trc_id')
                idenusers = LikedTrack.objects.all().filter(~Q(user_id=auth.get_user(request).id)).values_list('user_id', flat=True).distinct()
                chance = {}
                for user in idenusers:
                    tracks = LikedTrack.objects.all().filter(user_id=user).values_list('trc_id')
                    likes = ((math.fabs(len(set(likedtracks) & set(tracks)))) /
                             (math.fabs(len(set(likedtracks) | set(tracks)))))
                    chance[user] = likes
                chance = sorted(chance.items(), key=lambda item: -item[1])
                tracks = []
                for key in chance:
                    tracks += LikedTrack.objects.all().filter(user_id=key[0]).values_list('trc_id')
                identracks = []
                for track in tracks:
                    if track not in identracks and track not in historytracks and track not in likedtracks:
                        identracks.append(track[0])
                # tracks = Track.objects.all().filter(id__in=[l for l in identracks])
                # tracks = []
                # for track in identracks:
                #     trc = Track.objects.all().filter(id=track)
                #     tracks.append(trc)
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


def gettrack(authuser): #для Димы
    likedtracks = LikedTrack.objects.all().filter(user_id=authuser).values_list('trc_id')
    historytracks = TrackHistory.objects.all().filter(user_id=authuser).values_list('trc_id')
    idenusers = LikedTrack.objects.all().filter(~Q(user_id=authuser)).values_list('user_id', flat=True).distinct()
    chance = {}
    tracks = LikedTrack.objects.all().filter(user_id__in=idenusers).values_list('trc_id')
    for user in idenusers:
        likes = ((math.fabs(len(set(likedtracks) & set(tracks)))) /
                 (math.fabs(len(set(likedtracks) | set(tracks)))))
        chance[user] = likes
    chance = sorted(chance.items(), key=lambda item: -item[1])
    tracks = []
    for key in chance:
        tracks += LikedTrack.objects.all().filter(user_id=key[0]).values_list('trc_id')
    identracks = []
    for track in tracks:
        if track not in identracks and track not in historytracks and track not in likedtracks:
            identracks.append(track[0])
    tracks = Track.objects.all().filter(id=identracks[0])
    return tracks
'''@api_view(['GET'])
def track(request):
    if request.method == "GET":
        gen = request.query_params['genre']
        if gen == 'fav':
            likedtracks = LikedTrack.objects.all().filter(user_id=auth.get_user(request).id).values_list('trc_id')
            tracks = []
            for track in likedtracks:
                trc = Track.objects.all().get(id=track[0])
                tracks.append(trc)
        elif gen == 'rec':
            likedtracks = LikedTrack.objects.all().filter(user_id=auth.get_user(request).id).values_list('trc_id')
            users = LikedTrack.objects.all().values_list('user_id')
            idenusers = []
            for user in users:
                if user not in idenusers and user != auth.get_user(request).id:
                    idenusers.append(user)
            chance = {}
            for user in idenusers:
                tracks = LikedTrack.objects.all().filter(user_id=user).values_list('trc_id')
                likes = ((math.fabs(len(set(likedtracks) & set(tracks)))) /
                         (math.fabs(len(set(likedtracks) | set(tracks))))) / (len(idenusers) - 1)
                chance[user] = likes
            chance = sorted(chance.items(), key=lambda item: -item[1])
            tracks = []
            for key in chance:
                tracks += LikedTrack.objects.all().filter(user_id=key[0]).values_list('trc_id')
            identracks = []
            for track in tracks:
                if track not in identracks and track not in likedtracks:
                    identracks.append(track)
            tracks = []
            for track in identracks:
                trc = Track.objects.all().get(id=track[0])
                tracks.append(trc)
        else:
            # print(gen)
            # tracks = Track.objects.all().select_related('alb_id__per_id').values('name_trc', 'alb_id__image_alb',
            # 'alb_id__per_id__name_per', 'id')
            tracks = Track.objects.select_related('alb_id__stl_id__gnr_id').all().order_by('-rating_trc')
            if gen != 'all':
                tracks = tracks.filter(alb_id__stl_id__gnr_id_id=gen)

        serializer = NoLinkTrackSerializer(tracks, many=True)
        # json_jn = json.dumps(list(tracks), cls=DjangoJSONEncoder)
        # return HttpResponse(json_jn, content_type="application/json")
        return Response(serializer.data, status=status.HTTP_200_OK)'''


@api_view(['GET'])
def best_performer(request):
    if request.method == "GET":
        performer = Performer.objects.order_by('rating_per').reverse()[:3]
        serializer = PerformerSerializer(performer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        return Response({'month': monthS.data[0], 'week': monthS.data[1]}, status=status.HTTP_200_OK)


class Names:
    name_track = ""
    image_track = ""

    def __init__(self, name_track, image_track):
        self.name_track = name_track
        self.image_track = image_track


def load_music(request):
    return render(request, 'mainapp/loader-music.html')


def profile(request):
    return render(request, 'mainapp/profile.html')


@api_view(['POST', 'GET'])
def album(request):  # нужно сделать отдельный запрос для каждого трека, и тогда можно будет отслеживать процесс их загрузки
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


def music_group(request):
    return render(request, 'mainapp/musicgroup.html', {'performer': Performer.objects.all()})


@api_view(['GET'])
def track_attr(request):
    if request.method == "GET":
        id = request.query_params['id']
        track = TrackMethods.get(id)
        if track is not None:
            serializer = TrackSerializer(track)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
    def post(self, request, format=None):  # создание или изменение исполнителя
        name = request.POST["name"]
        try:
            label = request.FILES["label"]
        except MultiValueDictKeyError:
            label = None
        description = request.POST["description"]
        id = request.POST["id"]
        save_performer(id, auth.get_user(request).id, name, label, description)

        return Response(status=status.HTTP_200_OK)


class PerformerDetail(APIView):
    def get_object(self, pk):
        try:
            return Performer.objects.get(pk=pk)
        except Performer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if pk == 'me':  # получение исполнителя по пользователю
            user = auth.get_user(request).id
            performer = PerformerMethods.get(user)
            serializer = FullPerformerSerializer(performer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif re.fullmatch(r'[0-9]+', pk):
            performer = self.get_object(pk)
            serializer = FullPerformerSerializer(performer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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


@api_view(['PUT'])
def history(request):
    if request.method == 'PUT':
        result = TrackHistoryMethods.create(request.query_params['track_id'], auth.get_user(request).id)
        if result:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def login(request):
    if request.method == 'GET':
        return Response({'username': auth.get_user(request).username}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return Response({'username': auth.get_user(request).username}, status=status.HTTP_200_OK)
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
        return Response({'username': auth.get_user(request).username}, status=status.HTTP_200_OK)
