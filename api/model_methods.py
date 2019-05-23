# import datetime
import math
import random
import shutil
import os
import nmslib
import numpy as np
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.files import FieldFile, ImageFieldFile
from django.db.models import F, Q

from api.models import *


def get_random(all_tracks):  # возвращает рандомное значение из списка
    rand = random.randint(0, len(all_tracks) - 1)
    return all_tracks[rand]


class PerformerMethods:

    @staticmethod
    def create(user, name, description):
        # date = datetime.date.today()
        
        performer = Performer.objects.create(user_id=User.objects.get(pk=user), name_per=name, about_per=description)
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


class PlaylistMethods:
    @staticmethod
    def delete(id: int, per_id: Performer):
        try:
            playlist = Playlist.objects.get(pk=id, per_id=per_id)
            shutil.rmtree('./media/playlists/' + str(playlist.id))
            playlist.delete()
            return True
        except Playlist.DoesNotExist:
            return False


class TrackMethods:

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
            if LikedTrack.objects.filter(user_id=user, trc_id=track).count() == 0:
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
            if type(user_id) == User:
                LikedTrack.objects.get(user_id=user_id, trc_id=track_id)
                return True
            return False
        except ObjectDoesNotExist:
            return False


class LikedAlbumMethods:
    @staticmethod
    def check_if_liked(user_id, album_id):  # проверка лайкнут ли альбом
        try:
            if type(user_id) == User:
                LikedAlbum.objects.get(user_id=user_id, album_id=album_id)
                return True
            return False
        except ObjectDoesNotExist:
            return False


class LikedPlaylistMethods:
    @staticmethod
    def check_if_liked(user_id, playlist_id):  # проверка лайкнут ли альбом
        try:
            if type(user_id) == User:
                LikedPlaylist.objects.get(user_id=user_id, playlist_id=playlist_id)
                return True
            return False
        except ObjectDoesNotExist:
            return False


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
                    if count > 9:
                        hist.delete()
                        count -= 1
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


'''class TrackReportMethods:
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
            return False'''


class TrackRecommendation:

    @staticmethod
    def get_recommendation(user_id, limit, interval=None, genre_id=None, style_id=None):
        history_tracks = TrackHistory.objects.all().filter(user_id=user_id).values_list('trc_id')
        likes_kwargs = {}
        tracks_kwargs = {}

        if style_id is not None:
            likes_kwargs['trc_id__alb_id__stl_id'] = style_id
            tracks_kwargs['alb_id__stl_id'] = style_id,
        elif genre_id is not None:
            likes_kwargs['trc_id__alb_id__stl_id__gnr_id'] = genre_id
            tracks_kwargs['alb_id__stl_id__gnr_id'] = genre_id,

        if interval is not None:
            tracks_kwargs['date_trc__gte'] = date.today() - timedelta(days=int(interval))

        liked_tracks = LikedTrack.objects.filter(user_id=user_id, **likes_kwargs).values_list('trc_id', 'plays_amount')
        tracks = Track.objects.filter(~Q(id__in=history_tracks), **tracks_kwargs).values_list('id')
        track_ids = []
        if liked_tracks.count() > 0 and tracks.count() > 0:
            plays_amount = 0
            user_features = 0
            for liked_track in liked_tracks:
                this_features = np.load('features/' + str(liked_track[0]) + '.npy')
                this_features *= liked_track[1]
                user_features += this_features
                plays_amount += liked_track[1]
            user_features /= plays_amount

            features_list = []
            for track in tracks:
                features = np.load('features/' + str(track[0]) + '.npy')
                features_list.append(features)

            data = np.array(features_list)
            index = nmslib.init(method='hnsw', space='cosinesimil')
            index.addDataPointBatch(data)
            index.createIndex({'post': 2})

            # query for the nearest neighbours of the first datapoint
            ids, distances = index.knnQuery(user_features, k=limit)

            for id_ in ids:
                track_ids.append(tracks[int(id_)][0])

        # print(len(track_ids), track_ids)
        return track_ids

    '''@staticmethod
    def get_recommendation_old(authuser):
        userstracks = LikedTrack.objects.all().filter(~Q(user_id=authuser)).values_list('trc_id', 'user_id')
        likedtracks = LikedTrack.objects.all().filter(user_id=authuser).values_list('trc_id')
        historytracks = TrackHistory.objects.all().filter(user_id=authuser).values_list('trc_id')
        # reporttracks = TrackReport.objects.all().filter(user_id=authuser).values_list('trc_id')
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
        #print(dicttrack)
        tracks = []
        for track in dicttrack:
            tracks.append(int(track[0]))
        identracks = []
        #print(tracks)
        recommended_in_history = []
        for track in tracks:
            if (track,) not in identracks and (track,) not in historytracks:
                identracks.append(track)
            elif (track,) in historytracks:
                recommended_in_history.append((track,))
        rec_in_hist = TrackHistory.objects.filter(trc_id__in=recommended_in_history, user_id=authuser).order_by('id')
        for rec in rec_in_hist:
            if rec.trc_id.id in identracks:
                identracks.remove(rec.trc_id.id)
            identracks.append(rec.trc_id.id)
        #print(identracks)
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
        return dict'''
