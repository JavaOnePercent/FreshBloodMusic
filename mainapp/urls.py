from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_view, name='main_view'), # главная
    url(r'^next/$', views.next_track, name='next_track'), # запрос следующего трека
    url(r'^like/$', views.like, name='like'),  # обработка лайкусиков
]