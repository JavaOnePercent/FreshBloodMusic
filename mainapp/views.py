import random
import json
from django.shortcuts import render
from django.contrib import auth
from mainapp.models import Performer, Genre, Album, Track, LikedTrack
from django.http import HttpResponse

class Test:
    firstTrack = None #id первого и второго трека
    secondTrack = None #второй трек (отправляется сразу после первого)

def mainview(request): #главная. возвращает отрендеренный html с первым рандомным треком
    track = getTwo()
    Test.firstTrack = track[0].id
    Test.secondTrack = track[1].id

    return render(request, 'mainapp/homePage.html', {"track_name": track[0].name_trc, "performer_name": track[0].alb_id.per_id.name_per, "file_link": "/mainapp/album_sources/" + track[0].link_trc,
                                                     "logo_link": "/mainapp/album_sources/" + track[0].alb_id.image_alb,
                                                     "nextlogo_link": "/mainapp/album_sources/" + track[1].alb_id.image_alb, 'username': auth.get_user(request).username})

def first(request):  #отвечает на запрос сразу после загрузки первого трека
    json_data = json.dumps({"first_id": Test.firstTrack,"second_id": Test.secondTrack})
    return HttpResponse(json_data, content_type="application/json")

def nextTrack(request):  #запрос следующего трека
    parsedJson = json.loads(request.body)
    track = getTwo(parsedJson)

    json_data = json.dumps({"track_name": track[0].name_trc, "performer_name": track[0].alb_id.per_id.name_per,
                                "file_link": "/static/mainapp/album_sources/" + track[0].link_trc,
                                "logo_link": "/static/mainapp/album_sources/" + track[0].alb_id.image_alb,
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