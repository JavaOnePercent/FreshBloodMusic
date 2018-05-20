import math
import random

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.files import FieldFile, ImageFieldFile
from django.db.models import F, Q

from mainapp.models import Track, LikedTrack, Album, Performer, Genre, GenreStyle, TrackHistory, TrackReport


def get_random(all_tracks):  # возвращает рандомное значение из списка
    rand = random.randint(0, len(all_tracks) - 1)
    return all_tracks[rand]


class PerformerMethods:
    @staticmethod
    def create(id, user, name, description, date):
        performer = Performer.objects.update_or_create(id=id, defaults={'user_id': User.objects.get(pk=user),
                                                                        'name_per': name,
                                                                        'about_per': description,
                                                                        'date_per': date})
        return performer[0]

    @staticmethod
    def add_image(performer, image):
        field_file = FieldFile(performer, Performer.image_per.field, image)
        performer.image_per = field_file
        performer.save()

    @staticmethod
    def get(user):
        performer = Performer.objects.get(user_id=User.objects.get(pk=user))
        return performer


class AlbumMethods:
    @staticmethod
    def create(user, name, genre, date):
        album = Album(per_id=Performer.objects.get(user_id=user), name_alb=name,
                      stl_id=GenreStyle.objects.get(id=genre), image_alb='', date_alb=date)
        album.save()

        # album.image_alb = str(album.id) + '/logo.jpg'
        # album.save()
        return album

    @staticmethod
    def add_image(album, image_alb):
        field_file = FieldFile(album, Album.image_alb.field, image_alb)
        album.image_alb = field_file
        album.save()

    @staticmethod
    def get(user):
        performer = Performer.objects.get(user_id=user)
        albums = Album.objects.filter(per_id=Performer.objects.get(pk=performer))
        return albums


class TrackMethods:
    @staticmethod
    def create(album, name, date):
        track = Track(alb_id=album, name_trc=name, audio_trc='',
                      date_trc=date)
        track.save()
        # track.link_trc = str(album.id) + '/' + str(track.id) + '.mp3'
        # track.save()
        return track

    @staticmethod
    def add_audio(track, audio):
        field_file = FieldFile(track, Track.audio_trc.field, audio)
        track.audio_trc = field_file
        track.save()

    @staticmethod
    def get(id):
        try:
            return Track.objects.all().get(pk=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_two(parsed_json=None):
        # возвращает два трека рандомно (принимает json, в котором id текущего и следующего трека)

        all_tracks = Track.objects.all()
        tracks = []

        if parsed_json["next_track"] != '':
            tracks.append(all_tracks.get(pk=parsed_json["next_track"]))
            while tracks.__len__() == 1:
                track = get_random(all_tracks)
                if track != tracks[0] and str(track.id) != parsed_json["current_track"]:
                    tracks.append(track)
                    break
        else:
            tracks.append(get_random(all_tracks))
            while tracks.__len__() == 1:
                track = get_random(all_tracks)
                if track != tracks[0]:
                    tracks.append(track)
                    break

        return tracks


class GenreMethods:
    @staticmethod
    def get():
        return Genre.objects.all()


class GenreStyleMethods:
    @staticmethod
    def get(gnr_id):
        return GenreStyle.objects.filter(gnr_id=gnr_id)


class LikedTrackMethods:
    @staticmethod
    def get(user_id):
        user = User.objects.get(pk=user_id)
        likes = LikedTrack.objects.filter(user_id=user)
        return likes

    @staticmethod
    def add_like(track_id, user_id):  # добавление нового лайка в таблицу
        if track_id is not None and user_id is not None:
            track = Track.objects.get(pk=track_id)
            user = User.objects.get(pk=user_id)
            LikedTrack(user_id=user, trc_id=track).save()
            return True
        else:
            return False
    @staticmethod
    def add_increment(track_id):
        if track_id is not None:
            track = Track.objects.get(pk=track_id)
            performer = Performer.objects.get(pk=track.alb_id.per_id.id)
            Track.objects.filter(pk=track_id).update(rating_trc=F('rating_trc') + 1)
            Performer.objects.filter(pk=performer.id).update(rating_per=F('rating_per') + 1)
            return True
        else:
            return False

    @staticmethod
    def add_decrement(track_id):
        if track_id is not None:
            track = Track.objects.get(pk=track_id)
            performer = Performer.objects.get(pk=track.alb_id.per_id.id)
            if track.rating_trc > 0:
                Track.objects.filter(pk=track_id).update(rating_trc=F('rating_trc') - 1)
            if performer.rating_per > 0:
                Performer.objects.filter(pk=performer.id).update(rating_per=F('rating_per') - 1)
            return True
        else:
            return False


    @staticmethod
    def remove_like(track_id, user_id):  # удаление лайка из таблицы
        if track_id is not None and user_id is not None:
            track = Track.objects.get(pk=track_id)
            user = User.objects.get(pk=user_id)
            LikedTrack.objects.filter(user_id=user, trc_id=track).delete()
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


class TrackHistoryMethods:
    @staticmethod
    def create(track_id, user_id):  # добавление записи истории в таблицу
        if track_id is not None and user_id is not None:
            track = Track.objects.get(pk=track_id)
            user = User.objects.get(pk=user_id)
            count = TrackHistory.objects.filter(user_id=user).order_by('count').last()
            if count is None:
                count = 0
            TrackHistory(user_id=user, trc_id=track, count=count.count+1).save()
            return True
        else:
            return False


class TrackReportMethods:
    @staticmethod
    def create(track_id, user_id):  # добавление записи жалоб в таблицу
        if track_id is not None and user_id is not None:
            track = Track.objects.get(pk=track_id)
            user = User.objects.get(pk=user_id)
            report = TrackReport.objects.all().filter(user_id=user, trc_id=track)
            if not report:
                TrackReport(user_id=user, trc_id=track).save()
                return True
            else:
                return False
        else:
            return False

class TrackRecommendation:
    @staticmethod
    def get_recommendation(authuser):  # добавление записи жалоб в таблицу
        likedtracks = LikedTrack.objects.all().filter(user_id=authuser).values_list('trc_id')
        historytracks = TrackHistory.objects.all().filter(user_id=authuser).values_list('trc_id')
        reporttracks = TrackReport.objects.all().filter(user_id=authuser).values_list('trc_id')
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
            if track not in identracks and track not in historytracks and track not in likedtracks and track not in reporttracks:
                identracks.append(track[0])
        return identracks

