import datetime
import os
import re

from PIL import Image
from django.core.files.storage import FileSystemStorage
from pydub import AudioSegment

from mainapp.model_methods import AlbumMethods, TrackMethods


def save_album(user, name, genre, logo, tracks):  # сохранение альбома в БД и в файлы
    date = datetime.date.today()
    album = AlbumMethods.create(user=user, name=name, genre=genre, date=date)
    Compressor.dir = str(album.id) + '/'
    os.mkdir(Compressor.path + Compressor.dir)
    if logo is not None:
        image_alb = Compressor(logo.read(), logo.content_type, 'logo.jpg').compress()
        AlbumMethods.write_image_alb(album, image_alb)
    for track in tracks:
        tr_id = TrackMethods.create(album=album, name=track.name, date=date)
        audio = Compressor(track.read(), track.content_type, str(tr_id.id) + '.mp3').compress()
        TrackMethods.write_audio(tr_id, audio)
    Compressor.remove_temp()


class Compressor:
    path = './media/albums/'
    dir = ''

    def __init__(self, file_bytes, content_type, name):
        self.bytes = file_bytes
        self.type = content_type
        self.name = name

    def compress(self):
        if re.fullmatch(r'image/\S*', self.type):
            self.compress_image()
        elif re.fullmatch(r'audio/\S*', self.type):
            self.compress_audio()
        # f = open(self.path + self.dir + self.name, "rb")
        # f.close()
        return 'albums/' + self.dir + self.name

    def compress_image(self):
        src = self.save_temp()
        im = Image.open(src)
        im = im.resize((320, 320), Image.BICUBIC)
        im.save(self.path + self.dir + self.name, 'jpeg', quality=95, optimize=True)

    def compress_audio(self):
        src = self.save_temp()
        sound = AudioSegment.from_mp3(src)
        sound.export(self.path + self.dir + self.name, format="mp3", bitrate="128k")

    def save_temp(self):
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
            return False

