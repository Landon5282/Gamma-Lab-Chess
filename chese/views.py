from django.http import HttpResponse


def hello(request):
    return HttpResponse("Hello world ! ")

from django.shortcuts import render

def playChese(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'playChese.html', context)