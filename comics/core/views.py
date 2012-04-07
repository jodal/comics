from django.http import HttpResponse
from django.shortcuts import render


def about(request):
    return render(request, 'core/about.html', {'active': {'about': True}})


def robots(request):
    return HttpResponse('User-Agent: *\nDisallow: /\n', mimetype='text/plain')
