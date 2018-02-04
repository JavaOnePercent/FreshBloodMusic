from django.contrib import admin
from mainapp.models import Performer, Genre, Album, Track, LikedTrack

admin.site.register(Performer)
admin.site.register(Genre)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(LikedTrack)