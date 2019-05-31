from django.contrib import admin
from api.models import *

admin.site.register(Performer)
admin.site.register(Genre)
admin.site.register(GenreStyle)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(LikedAlbum)
admin.site.register(LikedTrack)
admin.site.register(TrackHistory)
admin.site.register(Playlist)
admin.site.register(PlaylistTrack)
admin.site.register(LikedPlaylist)
admin.site.register(TrackPlaysAmount)