from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.main_view, name='main_view'), # главная
    url(r'^performers/\d+$', views.main_view, name='main_view'),
    url(r'^login', views.main_view, name='main_view'),
    url(r'^register', views.main_view, name='main_view'),
    url(r'^settings', views.main_view, name='main_view'),
]