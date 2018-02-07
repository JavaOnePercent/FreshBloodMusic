from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^newperformer', views.newperformer, name='newperformer'),
    url(r'^', views.performers, name='performers'),
]