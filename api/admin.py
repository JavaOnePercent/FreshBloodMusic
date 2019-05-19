from django.contrib import admin
from api.models import *

admin.site.register(Performer)
admin.site.register(Genre)
admin.site.register(GenreStyle)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(LikedTrack)
admin.site.register(TrackHistory)