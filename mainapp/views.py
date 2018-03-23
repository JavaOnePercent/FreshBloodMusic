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
    return render(request, 'mainapp/homePage.html', {'username': auth.get_user(request).username})


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
        #gen = request.POST.get('gn', '')
        gen = 2
        tracks = Track.objects.all().filter(gnr_id = gen)
        name_track = tracks.values_list('name_trc')

        track_id = tracks.values('alb_id')
        image_track = []
        for track in track_id:
            image = Album.objects.get(pk=track["alb_id"]).image_alb
            image_track.append(image)
        json_jn = json.dumps({"names": list(name_track), "images": list(image_track)}, cls=DjangoJSONEncoder)
        return HttpResponse(json_jn, content_type="application/json")

def best_performer(request):
    if request.method == "GET":
        performer = Performer.objects.order_by('rating_per').reverse()[:3]
        performers = performer.values_list('name_per', 'image_per')
        #image_performer = performer.values_list('image_per')
        json_jn = json.dumps({"performers": list(performers)}, cls=DjangoJSONEncoder)
        return HttpResponse(json_jn, content_type="application/json")

def top_month(request):
    if request.method == "GET":
        name_track = Track.objects.order_by('rating_trc').reverse()[:1]
        track = name_track.values_list('name_trc', 'rating_trc')
        #rating = name_track.values_list('rating_trc')
        alb_id = name_track.values('alb_id')
        for alb in alb_id:
            image = Album.objects.get(pk = alb["alb_id"]).image_alb
            performer = Album.objects.get(pk = alb["alb_id"]).per_id.name_per
        month = [image, performer]
        json_jn = json.dumps({"track": track[0], "month": month}, cls=DjangoJSONEncoder)
        #json_jn = json.dumps({"name_track": list(name), "like_track": list(rating), "image_track": image, "performer_track": performer}, cls=DjangoJSONEncoder)
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
