import json
from django.shortcuts import render
from django.contrib import auth
from mainapp.models import Performer, Genre, Album, Track, LikedTrack
from django.http import HttpResponse

def main_view(request): # главная
    return render(request,'mainapp/homePage.html', {'username': auth.get_user(request).username})

def next_track(request):  # запрос следующего трека
    parsed_json = json.loads(request.body)
    tracks = Track.get_two(parsed_json)
    is_liked = LikedTrack.check_if_liked(auth.get_user(request).id, tracks.first.id)
    json_data = json.dumps({"track_name": tracks.first.name_trc, # имя трека
                                "performer_name": tracks.first.alb_id.per_id.name_per, # имя исполнителя
                                "file_link": "/static/mainapp/album_sources/" + tracks.first.link_trc, # ссылка на аудиофайл
                                "logo_link": "/static/mainapp/album_sources/" + tracks.first.alb_id.image_alb, # ссылка на лого ВОЗМОЖНО НЕ НУЖНО ЕЕ КАЖДЫЙ РАЗ ОТПРАВЛЯТЬ
                                "is_liked": is_liked, # лайкнут ли трек
                                "nextlogo_link": "/static/mainapp/album_sources/" + tracks.second.alb_id.image_alb, # ссылка на лого следующего трека
                                "current_id": tracks.first.id, # id текущего трека
                                "next_id": tracks.second.id, # id следующего трека
                            })
    return HttpResponse(json_data, content_type="application/json")

def like(request): # обработчик лайков
    parsed_json = json.loads(request.body)
    track_id = parsed_json["current_track"]
    user_id = auth.get_user(request).id
    if parsed_json["option"] == "add":  #добавление лайка
        result = LikedTrack.add_like(track_id, user_id)
        if result:
            json_data = json.dumps({"result": "added"})
        else:
            json_data = json.dumps({"result": "failure"})
    elif parsed_json["option"] == "remove":  #удаление лайка
        result = LikedTrack.remove_like(track_id, user_id)
        if result:
            json_data = json.dumps({"result": "removed"})
        else:
            json_data = json.dumps({"result": "failure"})
    else:
        json_data = json.dumps({"result": "failure"})
    return HttpResponse(json_data, content_type="application/json")



