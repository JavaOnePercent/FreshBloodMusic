from django.shortcuts import render
from django.contrib import auth

def mainview(request):
    track = {"track_name": "track_name", "performer_name": "performer_name",
             "file_link": "/mainapp/12.mp3"}
    return render(request, 'mainapp/homePage.html', {"track_name":track["track_name"], "performer_name": track["performer_name"], "file_link": track["file_link"], 'username': auth.get_user(request).username})
