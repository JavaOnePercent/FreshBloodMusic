import datetime
import os
import re
import io

from PIL import Image
from pydub import AudioSegment

from api.model_methods import AlbumMethods, TrackMethods, PerformerMethods
from api.models import *
from rest_framework.exceptions import ParseError
from django.db.models.fields.files import FieldFile


def save_track(alb_id, name, audio, performer):
    date = datetime.date.today()
    try:
        album = Album.objects.get(pk=alb_id, per_id=performer.id)
    except Album.DoesNotExist:
        raise ParseError('Album for the current user does not exist')
    directory = 'albums/' + str(album.id) + '/'
    track = Track.objects.create(alb_id=album, name_trc=name, date_trc=date)
    # track.save()
    directory += str(track.id) + '.mp3'
    duration = compress_audio(audio.read(), directory)
    track.duration = int(duration)
    track.save()
    TrackMethods.add_audio(track, directory)
    return track


def save_album(performer, name, genre, logo, description):  # сохранение альбома с треками в БД и в файлы
    date = datetime.date.today()
    if 'albums' not in os.listdir('media'):
        os.mkdir('media/albums')
    album = Album.objects.create(per_id=performer, name_alb=name, about_alb=description,
                                 stl_id=GenreStyle.objects.get(id=genre), image_alb='', date_alb=date)
    directory = 'albums/' + str(album.id) + '/'
    os.mkdir(path + directory)
    if logo is not None:
        directory += 'logo.jpg'
        compress_image(logo.read(), directory)
        # image_alb.set_name('logo.jpg')
        AlbumMethods.add_image(album, directory)

    return album


def save_playlist(user, title, image):  # сохранение альбома с треками в БД и в файлы
    # date = datetime.date.today()
    if 'playlists' not in os.listdir('media'):
        os.mkdir('media/playlists')
    playlist = Playlist.objects.create(per_id=user, title=title)
    directory = 'playlists/' + str(playlist.id) + '/'
    os.mkdir(path + directory)
    if image is not None:
        directory += 'logo.jpg'
        compress_image(image.read(), directory)
        # image_alb.set_name('logo.jpg')
        field_file = FieldFile(playlist, Playlist.image.field, directory)
        playlist.image = field_file
        playlist.save()

    return playlist


def save_performer(id, name, label, description, performer):
    performer = Performer.objects.get(id=id)
    if 'performers' not in os.listdir('media'):
        os.mkdir('media/performers')
    directory = 'performers/' + str(performer.id) + '/'
    is_new = try_mkdir(path + directory)
    if label is not None:
        directory += 'logo.jpg'
        compress_image(label.read(), directory)
        # image.set_name('logo.jpg')
        if is_new:
            PerformerMethods.add_image(performer, directory)


def try_mkdir(directory):
    try:
        os.mkdir(directory)
        return True
    except FileExistsError:
        return False


path = './media/'


'''def compress(data, type, dir, name):
    if re.fullmatch(r'image/\S*', type):
        compress_image(data, dir, name)
    elif re.fullmatch(r'audio/\S*', type):
        compress_audio(data, dir, name)
    return dir + name'''


def compress_image(data, file):
    im = Image.open(io.BytesIO(data))
    im = im.resize((320, 320), Image.BICUBIC)
    im.save(path + file, 'jpeg', quality=95, optimize=True)


def compress_audio(data, file):
    sound = AudioSegment.from_mp3(io.BytesIO(data))
    sound.export(path + file, format="mp3", bitrate="128k")
    return sound.duration_seconds

