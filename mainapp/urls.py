from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.mainview, name='mainview'),
    url(r'^next/$', views.nextTrack, name='nextTrack'), #запрос следующего трека
    url(r'^first/$', views.first, name='first'), #первый запрос (запрашивает id первого и второго треков)
    url(r'^like/$', views.like, name='like'),  #обработка лайкусиков
]