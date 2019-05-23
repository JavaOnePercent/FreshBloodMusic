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

    '''@staticmethod
    def get_tracks_by_ids(ids):
        ordering = 'FIELD(id, %s)' % ','.join(str(id_) for id_ in ids)
        return Track.objects.filter(pk__in=ids).extra(
            select={'ordering': ordering}, order_by=('ordering',))'''

    @staticmethod
    def calculate_recommendations(liked_tracks, tracks, limit):
        recommended_tracks = []
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

            if type(tracks[0]) == dict:
                for track in tracks:
                    features = np.load('features/' + str(track['id']) + '.npy')
                    features_list.append(features)
            else:
                for track in tracks:
                    features = np.load('features/' + str(track.id) + '.npy')
                    features_list.append(features)

            data = np.array(features_list)
            index = nmslib.init(method='hnsw', space='cosinesimil')
            index.addDataPointBatch(data)
            index.createIndex({'post': 2})

            # query for the nearest neighbours of the first datapoint
            ids, distances = index.knnQuery(user_features, k=limit)

            for id_ in ids:
                recommended_tracks.append(tracks[int(id_)])

            return recommended_tracks

    @staticmethod
    def filter_query_by_recommendation(user_id, tracks, length):
        if type(user_id) == User:
            liked_tracks = LikedTrack.objects.filter(user_id=user_id).values_list('trc_id', 'plays_amount')
            recommended_tracks = TrackRecommendation.calculate_recommendations(liked_tracks, tracks, length)
            return recommended_tracks
        else:
            return list(tracks.order_by('-rating_trc'))

    @staticmethod
    def get_recommendation(user_id, limit, interval=None, genre_id=None, style_id=None, added_tracks=None):
        likes_kwargs = {}
        tracks_kwargs = {}
        added_tracks_ids = []
        if added_tracks is not None:
            for track in added_tracks:
                added_tracks_ids.append(track.id)

        if style_id is not None:
            likes_kwargs['trc_id__alb_id__stl_id'] = style_id
            tracks_kwargs['alb_id__stl_id'] = style_id,
        elif genre_id is not None:
            likes_kwargs['trc_id__alb_id__stl_id__gnr_id'] = genre_id
            tracks_kwargs['alb_id__stl_id__gnr_id'] = genre_id,

        if interval is not None:
            tracks_kwargs['date_trc__gte'] = date.today() - timedelta(days=int(interval))

        if type(user_id) == User:
            history_tracks = TrackHistory.objects.all().filter(user_id=user_id).values_list('trc_id')
            avoided_tracks = []
            for track in history_tracks:
                avoided_tracks.append(track[0])
            avoided_tracks.extend(added_tracks_ids)

            liked_tracks = LikedTrack.objects.filter(user_id=user_id, **likes_kwargs).values_list('trc_id', 'plays_amount')
            tracks = Track.objects.filter(~Q(id__in=avoided_tracks), **tracks_kwargs)

            # query for the nearest neighbours of the first datapoint
            if limit == 'max':
                track_ids = TrackRecommendation.calculate_recommendations(liked_tracks, tracks, len(tracks))
            else:
                track_ids = TrackRecommendation.calculate_recommendations(liked_tracks, tracks, limit)
        else:
            return list(Track.objects.filter(~Q(id__in=added_tracks_ids), **tracks_kwargs).order_by('-rating_trc'))

        return track_ids
