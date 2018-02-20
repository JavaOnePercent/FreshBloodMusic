import random
import json
from django.shortcuts import render
from django.contrib import auth
from mainapp.models import Performer, Genre, Album, Track, LikedTrack
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class Test:
    firstTrack = None #id первого и второго трека
    secondTrack = None #второй трек (отправляется сразу после первого)

def mainview(request): #главная. возвращает отрендеренный html с первым рандомным треком. ЕГО РЕНДЕРИТЬ НЕ НУЖНО
    track = getTwo()
    Test.firstTrack = track[0].id
    Test.secondTrack = track[1].id

    return render(request, 'mainapp/homePage.html', {"track_name": track[0].name_trc, "performer_name": track[0].alb_id.per_id.name_per, "file_link": "/mainapp/album_sources/" + track[0].link_trc,
                                                     "logo_link": "/mainapp/album_sources/" + track[0].alb_id.image_alb,
                                                     "nextlogo_link": "/mainapp/album_sources/" + track[1].alb_id.image_alb, 'username': auth.get_user(request).username})

def first(request):  #отвечает на запрос сразу после загрузки первого трека
    is_liked = checkIfLiked(auth.get_user(request).id, Test.firstTrack)
    json_data = json.dumps({"first_id": Test.firstTrack, "is_liked": is_liked,"second_id": Test.secondTrack})
    return HttpResponse(json_data, content_type="application/json")

def nextTrack(request):  #запрос следующего трека
    parsedJson = json.loads(request.body)
    track = getTwo(parsedJson)
    is_liked = checkIfLiked(auth.get_user(request).id, track[0].id)
    json_data = json.dumps({"track_name": track[0].name_trc, "performer_name": track[0].alb_id.per_id.name_per,
                                "file_link": "/static/mainapp/album_sources/" + track[0].link_trc,
                                "logo_link": "/static/mainapp/album_sources/" + track[0].alb_id.image_alb,
                                "is_liked": is_liked,
                                "nextlogo_link": "/static/mainapp/album_sources/" + track[1].alb_id.image_alb,
                                "current_id": track[0].id, "next_id": track[1].id,
                            })
    return HttpResponse(json_data, content_type="application/json")

def getTwo(parsed_json = None):   #возвращает два трека рандомно (принимает json, в котором id текущего и следующего трека)

    allTracks = Track.objects.all()
    tracks = [None, None]

    if parsed_json is not None:
        tracks[0] = allTracks.get(pk = parsed_json["next_track"])
        while tracks[1] is None:
            track = getRandom(allTracks)
            if track != tracks[0] and track.id != parsed_json["current_track"]:
                tracks[1] = track
                break
    else:
        tracks[0] = getRandom(allTracks)
        while tracks[1] is None:
            track = getRandom(allTracks)
            if track != tracks[0]:
                tracks[1] = track
                break

    return tracks

def getRandom(allTracks):
    rand = random.randint(0, len(allTracks) - 1)
    return allTracks[rand]

def like(request):        #обработчик лайков
    track_id = json.loads(request.body)["current_track"]
    user_id = auth.get_user(request).id
    if track_id is not None and user_id is not None:
        track = Track.objects.get(pk=track_id)
        user = User.objects.get(pk=user_id)
        LikedTrack(user_id=user, trc_id=track).save()
        json_data = json.dumps({"result": "success"})
    else:
        json_data = json.dumps({"result": "failure"})
    return HttpResponse(json_data, content_type="application/json")


def checkIfLiked(user_id, track_id):    #проверка лайкнут ли трек
    try:
        is_liked = True
        LikedTrack.objects.get(user_id=user_id, trc_id=track_id)
    except ObjectDoesNotExist:
        is_liked = False
    return is_liked
