import datetime
import os
import re
import io

from PIL import Image
from pydub import AudioSegment

from api.model_methods import AlbumMethods, TrackMethods, PerformerMethods
from api.models import *
from rest_framework.exceptions import ParseError


def save_track(alb_id, name, audio, performer):
    date = datetime.date.today()
    try:
        album = Album.objects.get(pk=alb_id, per_id=performer.id)
    except Album.DoesNotExist:
        raise ParseError('Album for the current user does not exist')
    directory = 'albums/' + str(album.id) + '/'
    track = TrackMethods.create(album=album, name=name, date=date)
    audio = Compressor(audio.read(), audio.content_type, str(track.id) + '.mp3', directory).compress()
    TrackMethods.add_audio(track, audio)
    return track


def save_album(performer, name, genre, logo, description):  # сохранение альбома с треками в БД и в файлы
    date = datetime.date.today()
    album = Album.objects.create(per_id=performer.id, name_alb=name, about_alb=description,
                                 stl_id=GenreStyle.objects.get(id=genre), image_alb='', date_alb=date)
    directory = 'albums/' + str(album.id) + '/'
    os.mkdir(Compressor.path + directory)
    if logo is not None:
        image_alb = Compressor(logo.read(), logo.content_type, 'logo.jpg', directory).compress()
        AlbumMethods.add_image(album, image_alb)

    return album


def save_performer(id, name, label, description, performer):
    performer = Performer.objects.get(id=id)
    directory = 'performers/' + str(performer.id) + '/'
    is_new = try_mkdir(Compressor.path + directory)
    if label is not None:
        image = Compressor(label.read(), label.content_type, 'logo.jpg', directory).compress()
        if is_new:
            PerformerMethods.add_image(performer, image)


def try_mkdir(directory):
    try:
        os.mkdir(directory)
        return True
    except FileExistsError:
        return False


class Compressor:
    path = './media/'

    def __init__(self, file_bytes, content_type, name, dir):
        self.bytes = file_bytes
        self.type = content_type
        self.name = name
        self.dir = dir

    def compress(self):
        if re.fullmatch(r'image/\S*', self.type):
            self.compress_image()
        elif re.fullmatch(r'audio/\S*', self.type):
            self.compress_audio()
        return self.dir + self.name

    def compress_image(self):
        im = Image.open(io.BytesIO(self.bytes))
        im = im.resize((320, 320), Image.BICUBIC)
        im.save(self.path + self.dir + self.name, 'jpeg', quality=95, optimize=True)

    def compress_audio(self):
        sound = AudioSegment.from_mp3(io.BytesIO(self.bytes))
        sound.export(self.path + self.dir + self.name, format="mp3", bitrate="128k")

    """def save_temp(self):
        f = open('temp', "wb")
        f.write(self.bytes)
        f.close()
        return 'temp'

    @staticmethod
    def remove_temp():
        try:
            os.remove('temp')
            return True
        except FileNotFoundError:
            return False"""

