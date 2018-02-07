from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from mainapp.models import Performer, Genre, Album, Track, LikedTrack
from django.template.context_processors import csrf
from datetime import datetime

def performers(request):
    return render(request, 'mymusic/performerlist.html')
def newperformer(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        name_per = request.POST.get('name_per', '')
        about_per = request.POST.get('about_per', '')
        image_per = request.POST.get('image_per', '')
        if not name_per:
            args['per_error'] = "Не все поля заполнены"
            return render(request, 'mymusic/newperformer.html', args)
        else:
            user = User.objects.get(pk=int(auth.get_user(request).id))
            date = str(datetime.strftime(datetime.now(), "%Y-%m-%d"))
            slug = slug.replace(' ', '_')
            performer = Performer(user_id=user, name_per=name_per, image_per=image_per, about_per=about_per, date_per=date, slug=slug)
            performer.save()
            return redirect('/performers')
    else:
        return render(request, 'mymusic/newperformer.html', args)