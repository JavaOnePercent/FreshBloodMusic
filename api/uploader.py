import datetime
import os
import re
import io

from pprint import pprint
from PIL import Image
from pydub import AudioSegment

from api.model_methods import AlbumMethods, TrackMethods, PerformerMethods


def save_album(user, name, genre, logo, tracks, track_name):  # сохранение альбома в БД и в файлы
    date = datetime.date.today()
    album = AlbumMethods.create(user=user, name=name, genre=genre, date=date)
    directory = 'albums/' + str(album.id) + '/'
    os.mkdir(Compressor.path + directory)
    if logo is not None:
        image_alb = Compressor(logo.read(), logo.content_type, 'logo.jpg', directory).compress()
        AlbumMethods.add_image(album, image_alb)
    pprint(track_name)
    for i in range(len(tracks)):
        tr_id = TrackMethods.create(album=album, name=track_name[i], date=date)
        #pprint(track)
        audio = Compressor(tracks[i].read(), tracks[i].content_type, str(tr_id.id) + '.mp3', directory).compress()
        TrackMethods.add_audio(tr_id, audio)
    #Compressor.remove_temp()


def save_performer(id, name, label, description):
    performer = PerformerMethods.update(id=id, name=name, description=description)
    directory = 'performers/' + str(performer.id) + '/'
    is_new = try_mkdir(Compressor.path + directory)
    if label is not None:
        image = Compressor(label.read(), label.content_type, 'logo.jpg', directory).compress()
        if is_new:
            PerformerMethods.add_image(performer, image)
    #Compressor.remove_temp()


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
        # f = open(self.path + self.dir + self.name, "rb")
        # f.close()
        return self.dir + self.name

    def compress_image(self):
        #src = self.save_temp()
        im = Image.open(io.BytesIO(self.bytes))
        im = im.resize((320, 320), Image.BICUBIC)
        im.save(self.path + self.dir + self.name, 'jpeg', quality=95, optimize=True)

    def compress_audio(self):
        #src = self.save_temp()
        #print(len(self.bytes))
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

