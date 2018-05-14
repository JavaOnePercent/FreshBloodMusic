from django.contrib import admin
from mainapp.models import Performer, Genre, GenreStyle, Album, Track, LikedTrack, TrackHistory

admin.site.register(Performer)
admin.site.register(Genre)
admin.site.register(GenreStyle)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(LikedTrack)
admin.site.register(TrackHistory)