import json
import os
import re
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.contrib import auth
from django.utils.datastructures import MultiValueDictKeyError

from .models import Performer, Genre, Album, Track, LikedTrack
from django.http import HttpResponse
from .uploader import Compressor, save_album
from .serializers import TrackSerializer, NoLinkTrackSerializer
from .model_methods import TrackMethods, LikedTrackMethods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import math


def main_view(request):  # главная
    return render(request, 'mainapp/homePage.html', {'username': auth.get_user(request).username, 'genre': Genre.objects.all()})


@api_view(['GET'])  # запрос следующего трека
def next_track(request):
    if request.method == 'GET':
        tracks = TrackMethods.get_two(request.query_params)
        is_liked = LikedTrackMethods.check_if_liked(auth.get_user(request).id, tracks[0].id)
        serializer = TrackSerializer(tracks, many=True)
        serializer.data[0]["is_liked"] = is_liked
        return Response({'current': serializer.data[0], 'next': serializer.data[1]}, status=status.HTTP_200_OK)


@api_view(['PUT', 'DELETE'])  # обработчик лайков
def like(request):
    if request.method == 'PUT':  # добавление лайка
        result = LikedTrackMethods.add_like(request.query_params['track_id'], auth.get_user(request).id)
        if result:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':  # удаление лайка
        result = LikedTrackMethods.remove_like(request.query_params['track_id'], auth.get_user(request).id)
        if result:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
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
        #print(gen)
        #tracks = Track.objects.all().select_related('alb_id__per_id').values('name_trc', 'alb_id__image_alb',
                                                                                  #'alb_id__per_id__name_per', 'id')
            tracks = Track.objects.all().order_by('-rating_trc')
            if gen != 'all':
                tracks = tracks.filter(gnr_id=gen)

        serializer = NoLinkTrackSerializer(tracks, many=True)
        #json_jn = json.dumps(list(tracks), cls=DjangoJSONEncoder)
        #return HttpResponse(json_jn, content_type="application/json")
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def best_performer(request):
    if request.method == "GET":
        performer = Performer.objects.order_by('rating_per').reverse()[:3].values_list('name_per', 'image_per')
        json_jn = json.dumps({"performers": list(performer)}, cls=DjangoJSONEncoder)
        return HttpResponse(json_jn, content_type="application/json")


@api_view(['GET'])
def top_month(request):
    if request.method == "GET":
        month = Track.objects.order_by('rating_trc').reverse()[:1].select_related('alb_id__per_id').values_list('name_trc', 'rating_trc', 'alb_id__image_alb', 'alb_id__per_id__name_per')
        json_jn = json.dumps({"month": list(month)}, cls=DjangoJSONEncoder)
        return HttpResponse(json_jn, content_type="application/json")


class Names:
    name_track = ""
    image_track = ""
    def __init__(self, name_track, image_track):
        self.name_track = name_track
        self.image_track = image_track


def load_music(request):
    return render(request, 'mainapp/loader-music.html')


@api_view(['POST'])
def album(request):  # нужно сделать отдельный запрос для каждого трека, и тогда можно будет отслеживать процесс их загрузки
    if request.method == 'POST':
        album_name = request.POST["name"]
        try:
            photo = request.FILES["photo"]
        except MultiValueDictKeyError:
            photo = None
        tracks = request.FILES.getlist('track')

        save_album(user=auth.get_user(request).id, name=album_name, logo=photo, tracks=tracks)

        return HttpResponse(status=200)


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
