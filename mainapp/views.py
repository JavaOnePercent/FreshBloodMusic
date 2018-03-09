import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.contrib import auth
from mainapp.models import Performer, Genre, Album, Track, LikedTrack
from django.http import HttpResponse

def main_view(request): # главная
    return render(request,'mainapp/homePage.html', {'username': auth.get_user(request).username, 'genre': Genre.objects.all()})

def next_track(request):  # запрос следующего трека
    new_data = request.body.decode("utf-8", "strict")
    parsed_json = json.loads(new_data)
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

def change_genre(request):
    if request.method == "POST":
        gen = request.POST.get('gn', '')
        tracks = Track.objects.all().filter(gnr_id = gen)
        name_track = tracks.values_list('name_trc')

        track_id = tracks.values('alb_id')
        image_track = []
        for track in track_id:

            image = Album.objects.get(pk=track["alb_id"]).image_alb
            image_track.append(image)
        json_jn = json.dumps({"names": list(name_track), "images": image_track}, cls=DjangoJSONEncoder)
        return HttpResponse(json_jn, content_type="application/json")

def best_performer(request):
    if request.method == "POST":
        performer = Performer.objects.order_by('rating_per').reverse()[:3]
        name_performer = performer.values_list('name_per')
        image_performer = performer.values_list('image_per')
        json_jn = json.dumps({"names": list(name_performer), "images": list(image_performer)}, cls=DjangoJSONEncoder)
        return HttpResponse(json_jn, content_type="application/json")

def top_month(request):
    if request.method == "POST":
        name_track = Track.objects.order_by('rating_trc').reverse()[:1]
        name = name_track.values_list('name_trc')
        rating = name_track.values_list('rating_trc')
        alb_id = name_track.values('alb_id')
        for alb in alb_id:
            image = Album.objects.get(pk = alb["alb_id"]).image_alb
            performer = Album.objects.get(pk = alb["alb_id"]).per_id.name_per
        json_jn = json.dumps({"name_track": list(name), "like_track": list(rating), "image_track": image, "performer_track": performer}, cls=DjangoJSONEncoder)
        return HttpResponse(json_jn, content_type="application/json")

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

class Names:
    name_track = ""
    image_track = ""
    def __init__(self, name_track, image_track):
        self.name_track = name_track
        self.image_track = image_track