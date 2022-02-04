from json import JSONDecoder
from django.http import HttpResponse, JsonResponse


def hello(request):
    return HttpResponse("Hello world ! ")

from django.shortcuts import render
import numpy as np

N = 5  # N*N
chessboard = np.ones((N, N))


def playChese(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'playChese.html', context)

def get_size(request):
    global N
    global chessboard
    chessboard = np.ones((N, N))
    chessboard[int(N / 2), int(N / 2)] = 0

    return HttpResponse(chessboard)

def get_coordinate(request):
    coordinate = JSONDecoder(request)
    # 拿起棋子
    if coordinate['flag'] == 0:
        chessboard[coordinate['x']][coordinate['y']] = 0
    # 落下棋子
    if coordinate['flag'] == 1:
        chessboard[coordinate['x']][coordinate['y']] = 1
    return JsonResponse(chessboard)