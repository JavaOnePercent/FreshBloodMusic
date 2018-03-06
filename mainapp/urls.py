from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_view, name='main_view'), # главная
    url(r'^change_genre/$', views.change_genre, name='change_genre'),
    url(r'^best_performer/$', views.best_performer, name='best_performer'),
    url(r'^top_month/$', views.top_month, name='top_month'),
    url(r'^next/$', views.next_track, name='next_track'), # запрос следующего трека
    url(r'^like/$', views.like, name='like'),  # обработка лайкусиков
]