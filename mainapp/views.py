from django.http import HttpResponse


def main_view(request):  # главная
    file = open('./mainapp/static/mainapp/index.html', 'r')
    index = file.read()
    file.close()
    return HttpResponse(index, content_type="text/html")