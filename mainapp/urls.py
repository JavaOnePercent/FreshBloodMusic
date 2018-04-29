from django.conf.urls import url
from . import views
from django.views.generic import ListView, DetailView
from mainapp.models import Performer

urlpatterns = [
    url(r'^$', views.main_view, name='main_view'), # главная
    url(r'^track$', views.track, name='track'),
    url(r'^best_performer/$', views.best_performer, name='best_performer'),
    url(r'^top_month/$', views.top_month, name='top_month'),
    url(r'^next$', views.next_track, name='next_track'),  # запрос следующего трека
    url(r'^likes$', views.likes, name='likes'),  # обработка лайкусиков
    url(r'^track_attr$', views.track_attr, name='track_attr'),
    url(r'^loader-music/$', views.load_music, name='load_music'),
    url(r'^profile/$', views.profile, name='profile'),
    # url(r'^add_album/$', views.add_album, name='add_album'),
    url(r'^album$', views.album, name='album'),
    url(r'^performers$', views.PerformersList.as_view()),
    url(r'^performers/(?P<pk>\w+)/$', views.PerformerDetail.as_view()),
    # url(r'^performers$', views.performers, name='performers'),
    url(r'^genre$', views.genre, name='genre'),
    # url(r'^performer/$', ListView.as_view(queryset=Performer.objects.all(), template_name="mainapp/musicgroup.html")),
    # url(r'^performer/(?P<slug>\w+)', DetailView.as_view(model = Performer, template_name = "mainapp/musicgroup.html")),
]