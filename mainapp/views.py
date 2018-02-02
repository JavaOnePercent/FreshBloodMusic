from django.shortcuts import render

def mainview(request):
    return render(request, 'mainapp/homePage.html')
