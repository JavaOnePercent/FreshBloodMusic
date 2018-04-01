import json
import os
import re
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.contrib import auth
from .models import Performer, Genre, Album, Track, LikedTrack
from django.http import HttpResponse
from .compressor import compress_image, compress_audio
from .serializers import TrackSerializer
from .model_methods import TrackMethods, LikedTrackMethods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def main_view(request):  # главная
    return render(request, 'mainapp/homePage.html', {'username': auth.get_user(request).username, 'genre': Genre.objects.all()})


@api_view(['POST'])  # запрос следующего трека
def next_track(request):
    if request.method == 'POST':
        tracks = TrackMethods.get_two(request.data)
        is_liked = LikedTrackMethods.check_if_liked(auth.get_user(request).id, tracks[0].id)
        serializer = TrackSerializer(tracks, many=True)
        serializer.data[0]["is_liked"] = is_liked
        return Response({'current': serializer.data[0], 'next': serializer.data[1]}, status=status.HTTP_200_OK)


@api_view(['POST', 'PUT'])  # обработчик лайков
def like(request):
    if request.method == 'PUT':  # добавление лайка
        result = LikedTrackMethods.add_like(request.data['track_id'], auth.get_user(request).id)
        if result:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':  # удаление лайка
        result = LikedTrackMethods.remove_like(request.data['track_id'], auth.get_user(request).id)
        if result:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

def change_genre(request):
    if request.method == "GET":
        gen = request.GET.get('genre', None)
        tracks = Track.objects.all().select_related('alb_id__per_id').values_list('name_trc', 'alb_id__image_alb', 'alb_id__per_id__name_per').filter(gnr_id=gen)
        json_jn = json.dumps({"genre": list(tracks)}, cls=DjangoJSONEncoder)
        return HttpResponse(json_jn, content_type="application/json")

def best_performer(request):
    if request.method == "GET":
        performer = Performer.objects.order_by('rating_per').reverse()[:3].values_list('name_per', 'image_per')
        json_jn = json.dumps({"performers": list(performer)}, cls=DjangoJSONEncoder)
        return HttpResponse(json_jn, content_type="application/json")

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

def add_album(request):
    if request.method == 'POST':
        path = './mainapp/static/mainapp/album_sources/'
        album_name = request.POST["name"]
        os.mkdir(path + album_name)
        path += album_name + '/'
        photo = request.FILES["photo"]
        track = request.FILES["track"]
        if re.fullmatch(r'image/\S*', photo.content_type):
            uploadedPic = path + "pic"
            f = open(uploadedPic, "wb")
            f.write(photo.read())
            f.close()
            compress_image(uploadedPic, path + 'pic.jpg')
            os.remove(uploadedPic)
        if re.fullmatch(r'audio/\S*', track.content_type):
            uploadedAudio = path + "audio"
            f = open(uploadedAudio, "wb")
            f.write(track.read())
            f.close()
            compress_audio(uploadedAudio, path + 'audio.mp3')
            os.remove(uploadedAudio)

    return HttpResponse(status=200)
