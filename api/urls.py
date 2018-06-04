from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^token$', views.get_token, name='get_token'),  # token
    url(r'^tracks$', views.TrackOverview.as_view(), name='tracks'),
    url(r'^tracks/(?P<pk>\w+)$', views.TrackDetail.as_view()),
    url(r'^top$', views.top, name='top'),
    # url(r'^next$', views.next_track, name='next_track'),  # запрос следующего трека
    url(r'^likes$', views.likes, name='likes'),  # обработка лайкусиков
    # url(r'^add_album/$', views.add_album, name='add_album'),
    url(r'^albums$', views.albums, name='albums'),
    url(r'^performers$', views.PerformersList.as_view()),
    url(r'^performers/(?P<pk>\w+)$', views.PerformerDetail.as_view()),
    url(r'^genre$', views.genre, name='genre'),
    url(r'^history$', views.history, name='history'),
    url(r'^report$', views.report, name='report'),

    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register', views.register, name='register'),
]