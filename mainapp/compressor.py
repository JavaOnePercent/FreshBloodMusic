from PIL import Image
from pydub import AudioSegment


def compress_image(src, dest):
    im = Image.open(src)
    im = im.resize((320,320), Image.BICUBIC)
    im.save(dest, 'jpeg', quality=95, optimize=True)


#compress_image("./static/mainapp/album_sources/govno.jpg", "./static/mainapp/album_sources/govno1.jpg")


def compress_audio(src, dest):
    sound = AudioSegment.from_mp3(src)
    sound.export(dest,
                 format="mp3", bitrate="128k")


#compress_audio("./static/mainapp/album_sources/HM_OST/02. M.O.O.N - Hydrogen.mp3",
               #"./static/mainapp/album_sources/HM_OST/02. M.O.O.N - Hydrogen1.mp3")