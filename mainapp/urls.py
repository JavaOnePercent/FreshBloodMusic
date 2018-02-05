from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.mainview, name='mainview'),
    url(r'^next/$', views.nextTrack, name='nextTrack'),
    url(r'^first/$', views.first, name='first'), #первый запрос (запрашивает id первого и второго треков)
]