import datetime
import math
import random
import shutil
import os

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.files import FieldFile, ImageFieldFile
from django.db.models import F, Q

from api.models import Track, LikedTrack, Album, Performer, Genre, GenreStyle, TrackHistory, TrackReport


def get_random(all_tracks):  # возвращает рандомное значение из списка
    rand = random.randint(0, len(all_tracks) - 1)
    return all_tracks[rand]


class PerformerMethods:
    @staticmethod
    def update(id, name, description):
        date = datetime.date.today()
        performer = Performer.objects.filter(id=id)
        performer.update(name_per=name, about_per=description, date_per=date)
        return performer[0]

    @staticmethod
    def create(user, name, description):
        date = datetime.date.today()
        
        performer = Performer.objects.create(user_id=User.objects.get(pk=user), name_per=name, about_per=description, date_per=date)
        is_new = try_mkdir('./media/performers/' + str(performer.id))
        shutil.copy(r'./mainapp/static/mainapp/images/cat.jpg', './media/performers/' + str(performer.id) + '/logo.jpg')
        performer = PerformerMethods.add_image(performer, 'performers/' + str(performer.id) + '/logo.jpg')
        return performer

    @staticmethod
    def add_image(performer, image):
        field_file = FieldFile(performer, Performer.image_per.field, image)
        performer.image_per = field_file
        performer.save()
        return performer

    @staticmethod
    def get(user):
        performer = Performer.objects.get(user_id=User.objects.get(pk=user))
        return performer

def try_mkdir(directory):
    try:
        os.mkdir(directory)
        return True
    except FileExistsError:
        return False

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

    @staticmethod
    def delete(id, user_id):
        try:
            album = Album.objects.get(pk=id)
            if user_id == album.per_id.user_id.id:
                Track.objects.filter(alb_id=album).delete()
                shutil.rmtree('./media/albums/' + str(album.id))
                album.delete()
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False


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
            return Track.objects.get(pk=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete(id, user_id):
        try:
            track = Track.objects.get(pk=id)
            if user_id == track.alb_id.per_id.user_id.id:
                track.delete()
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False


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
    def get(per_id):
        user = Performer.objects.get(pk=per_id).user_id
        likes = LikedTrack.objects.filter(user_id=user)
        return likes

    @staticmethod
    def likesAmount(track):
        trc = Track.objects.get(pk=track)
        likes = LikedTrack.objects.filter(trc_id=trc)
        return likes.count()

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

            history = TrackHistory.objects.filter(user_id=user).order_by('id')
            last = history.last()
            if last is not None:
                last = last.id
                count = history.count()
                for hist in history:
                    if count > 49:
                        hist.delete()  # здесь бы надо закодить, чтобы переписывать старые записи из таблицы, а не все время плодить новые индексы
                        count -= 1
            '''for index, hist in enumerate(history):
                if hist != history.last():
                    TrackHistory.objects.filter(id=hist.id + 1).update(user_id=hist.user_id, trc_id=hist.trc_id)
                else:
                    TrackHistory.objects.filter(id=hist.id + 1).update(user_id=hist.user_id, trc_id=hist.trc_id)'''
            TrackHistory.objects.filter(user_id=user, trc_id=track).delete()
            TrackHistory(user_id=user, trc_id=track).save()
            return True
        else:
            return False

    @staticmethod
    def get(user_id):
        user = User.objects.get(pk=user_id)
        tracks = TrackHistory.objects.filter(user_id=user).order_by('id').reverse()[:11]
        return tracks


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
    def get_recommendation(authuser):
        userstracks = LikedTrack.objects.all().filter(~Q(user_id=authuser)).values_list('trc_id', 'user_id')
        likedtracks = LikedTrack.objects.all().filter(user_id=authuser).values_list('trc_id')
        historytracks = TrackHistory.objects.all().filter(user_id=authuser).values_list('trc_id')
        reporttracks = TrackReport.objects.all().filter(user_id=authuser).values_list('trc_id')
        liked = []
        noauthtracks = []
        for track in userstracks:
            if (track[0],) not in likedtracks:
                noauthtracks.append(track)
        for auth in likedtracks:
            liked.append(auth[0])
        dict = TrackRecommendation.dict_trans(userstracks)
        dictiden = TrackRecommendation.dictiden_trans(noauthtracks)
        dicttrack = {}
        likes = 0
        for d in dictiden.keys():
            for u in dictiden[d]:
                likes = likes + ((math.fabs(len(set(liked) & set(dict[str(u)])))) /
                                 (math.fabs(len(set(liked) | set(dict[str(u)])))))
            likes = likes / len(dictiden[d])
            dicttrack.update({str(d): likes})
            likes = 0
        dicttrack = sorted(dicttrack.items(), key=lambda item: -item[1])
        print(dicttrack)
        tracks = []
        for track in dicttrack:
            tracks.append(int(track[0]))
        identracks = []
        print(tracks)
        recommended_in_history = []
        for track in tracks:
            if (track,) not in identracks and (track,) not in historytracks and (track,) not in reporttracks:
                identracks.append(track)
            elif (track,) in historytracks:
                recommended_in_history.append((track,))
        rec_in_hist = TrackHistory.objects.filter(trc_id__in=recommended_in_history, user_id=authuser).order_by('id')
        for rec in rec_in_hist:
            if rec.trc_id.id in identracks:
                identracks.remove(rec.trc_id.id)
            identracks.append(rec.trc_id.id)
        print(identracks)
        return identracks

    @staticmethod
    def dict_trans(tuple):
        dict = {}
        for iden in tuple:
            if str(iden[1]) not in dict.keys():
                dict.update({str(iden[1]): [iden[0]]})
            else:
                dict[str(iden[1])].append(iden[0])
        return dict

    @staticmethod
    def dictiden_trans(tuple):
        dict = {}
        for iden in tuple:
            if str(iden[0]) not in dict.keys():
                dict.update({str(iden[0]): [iden[1]]})
            else:
                dict[str(iden[0])].append(iden[1])
        return dict
