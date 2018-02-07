from django.conf.urls import url
from . import views
from django.views.generic import ListView, DetailView
from mainapp.models import Performer

urlpatterns = [
    url(r'^$', ListView.as_view(queryset=Performer.objects.all(), template_name="musicgroup/musicgroup.html")),
    url(r'^(?P<slug>\w+)', DetailView.as_view(model = Performer, template_name = "musicgroup/musicgroup.html")),
]