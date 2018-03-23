import random

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from mainapp.models import Track, LikedTrack


def get_random(all_tracks):  # возвращает рандомное значение из списка
    rand = random.randint(0, len(all_tracks) - 1)
    return all_tracks[rand]


class TrackMethods:
    @staticmethod
    def get_two(parsed_json=None):
        # возвращает два трека рандомно (принимает json, в котором id текущего и следующего трека)

        all_tracks = Track.objects.all()
        tracks = []

        if parsed_json is not None and parsed_json["next_track"] is not None:
            tracks.append(all_tracks.get(pk=parsed_json["next_track"]))
            while tracks.__len__() == 1:
                track = get_random(all_tracks)
                if track != tracks[0] and track.id != parsed_json["current_track"]:
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


class LikedTrackMethods:
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

