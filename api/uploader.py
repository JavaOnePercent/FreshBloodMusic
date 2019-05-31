import os
import io

from PIL import Image
from pydub import AudioSegment

from api.model_methods import AlbumMethods, TrackMethods, PerformerMethods
from api.models import *
from rest_framework.exceptions import ParseError
from django.db.models.fields.files import FieldFile
from FreshBloodMusic.apps import KerasConfig


def save_track(alb_id, name, audio, performer):
    try:
        album = Album.objects.get(pk=alb_id, per_id=performer.id)
    except Album.DoesNotExist:
        raise ParseError('Album for the current user does not exist')
    directory = 'albums/' + str(album.id) + '/'
    track = Track.objects.create(alb_id=album, name_trc=name)
    # track.save()
    directory += str(track.id) + '.mp3'
    duration = compress_audio(audio.read(), directory, str(track.id))
    track.duration = int(duration)
    track.save()
    TrackMethods.add_audio(track, directory)
    return track


def save_album(performer, name, genre, logo, description):  # сохранение альбома с треками в БД и в файлы
    # date = datetime.datetime.now()
    album = Album.objects.create(per_id=performer, name_alb=name, about_alb=description,
                                 stl_id=GenreStyle.objects.get(id=genre), image_alb='')
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


def save_performer(name, label, description, performer):
    # performer = Performer.objects.get(id=id)
    performer.name_per = name
    performer.about_per = description
    performer.save()

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
    im: Image = Image.open(io.BytesIO(data))
    if im.width > im.height:
        big = im.width
        small = im.height
        left = int((big - small) / 2)
        box = (left, 0, left + small, small)
    else:
        big = im.height
        small = im.width
        top = int((big - small) / 2)
        box = (0, top, small, top + small)

    im = im.crop(box)
    im = im.resize((320, 320), Image.BICUBIC)
    im = im.convert('RGB')
    im.save(path + file, 'jpeg', quality=95, optimize=True)


def compress_audio(data, file, track_id):
    sound = AudioSegment.from_mp3(io.BytesIO(data))
    sound.export(path + file, format="mp3", bitrate="128k")
    KerasConfig.model.predict_features(path + file, 'features/' + track_id + '.npy')
    return sound.duration_seconds

