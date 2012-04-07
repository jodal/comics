from django.http import HttpResponse


def robots(request):
    return HttpResponse('User-Agent: *\nDisallow: /\n', mimetype='text/plain')
