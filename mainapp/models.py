from django.db import models
import random
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
#from django.contrib import auth

class Performer(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='userperformer')
    name_per = models.CharField(max_length=30, unique=True)
    rating_per = models.IntegerField(default=0)
    image_per = models.CharField(max_length=50, default='0')
    about_per = models.TextField(null=True, blank=True)
    date_per = models.DateField(null=True, blank=True)
    slug = models.SlugField(max_length=30, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name_per

class Genre(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name_gnr = models.CharField(max_length=30)

    def __str__(self):
        return self.name_gnr

class Album(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    per_id = models.ForeignKey(Performer, on_delete=models.CASCADE, related_name='performeralbum')
    name_alb = models.CharField(max_length=30)
    gnr_id = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='albumgenre')
    numplays_alb = models.IntegerField(default=0)
    rating_alb = models.IntegerField(default=0)
    image_alb = models.CharField(max_length=50, default='0')
    date_alb = models.DateField()
    slug = models.SlugField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name_alb

class Track(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    alb_id = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='albumtrack')
    name_trc = models.CharField(max_length=50)
    gnr_id = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='trackgenre')
    link_trc = models.CharField(max_length=50)
    numplays_trc = models.IntegerField(default=0)
    rating_trc = models.IntegerField(default=0)
    date_trc = models.DateField()

    def __str__(self):
        return self.name_trc

    @staticmethod
    def get_two(parsed_json=None):  # возвращает два трека рандомно (принимает json, в котором id текущего и следующего трека)

        allTracks = Track.objects.all()
        tracks = TwoTracks()

        if parsed_json is not None and parsed_json["next_track"] is not None:
            tracks.first = allTracks.get(pk=parsed_json["next_track"])
            while tracks.second is None:
                track = get_random(allTracks)
                if track != tracks.first and track.id != parsed_json["current_track"]:
                    tracks.second = track
                    break
        else:
            tracks.first = get_random(allTracks)
            while tracks.second is None:
                track = get_random(allTracks)
                if track != tracks.first:
                    tracks.second = track
                    break

        return tracks


class LikedTrack(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='userliked')
    trc_id = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='trackliked')

    def __str__(self):
        return self.id

    @staticmethod
    def add_like(track_id, user_id): #добавление нового лайка в таблицу
        if track_id is not None and user_id is not None:
            track = Track.objects.get(pk=track_id)
            user = User.objects.get(pk=user_id)
            LikedTrack(user_id=user, trc_id=track).save()
            return True
        else:
            return False

    @staticmethod
    def check_if_liked(user_id, track_id):  # проверка лайкнут ли трек
        try:
            is_liked = True
            LikedTrack.objects.get(user_id=user_id, trc_id=track_id)
        except ObjectDoesNotExist:
            is_liked = False
        return is_liked


class TwoTracks:
    first = None  # id первого трека
    second = None  # id второго трека

def get_random(allTracks):  # возвращает рандомное значение из списка
    rand = random.randint(0, len(allTracks) - 1)
    return allTracks[rand]






