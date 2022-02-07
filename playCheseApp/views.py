from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
import numpy as np

from .models import Size

# 全局变量
N = 5  # N*N
chessboard = np.ones((N, N))
chessboard[int(N / 2), int(N / 2)] = 0
x1, x2, y1, y2 = 0, 0, 0, 0


@require_http_methods(["GET"])
def get_piece_array(request):
    arr = np.ones((15, 15)) 
    return JsonResponse(arr.tolist(), safe=False)


@require_http_methods(["GET"])
def restart(request):
    response = {}
    print(chessboard)
    try:
        response['error_num'] = 0
        response['msg'] = 'success'
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

@require_http_methods(["GET"])
def make_size(request):
    response = {}
    size = Size(size=5)
    try:
        t = int(request.GET.get('size'))
        global N
        global chessboard
        N = t
        chessboard = np.ones((N, N))
        chessboard[int(N / 2), int(N / 2)] = 0
        print(chessboard)
        size = Size(size=t)
        response['size'] = str(t)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def sendPos(request):
    response = {}
    move = 0
    try:
        global x1, x2, y1, y2
        # 前端比后端坐标多1
        x1 = int(request.GET.get('x1'))-1
        y1 = int(request.GET.get('y1'))-1
        x2 = int(request.GET.get('x2'))-1
        y2 = int(request.GET.get('y2'))-1
        print('x1:', x1, ' y1:', y1, ' x2:', x2, ' y2:', y2)
        # 判断是否可以移动
        if chessboard[x2][y2] == 0 and chessboard[x1][y1] == 1 and chessboard[int((x1+x2)/2)][int((y1+y2)/2)] == 1:
            move = 1
            chessboard[x1][y1] = 0
            chessboard[x2][y2] = 1
            a1, b1 = x2, y2
            # 判断移动模式
            if x1 == x2:
                if y1 > y2:  # 下移
                    chessboard[x1][y2+1] = 0
                    a2, b2 = x1, y2+1
                else:   # 上移
                    chessboard[x1][y1+1] = 0
                    a2, b2 = x1, y1+1
            elif y1 == y2:
                if x1 > x2:  # 左移
                    chessboard[x2+1][y1] = 0
                    a2, b2 = x2+1, y1
                else:  # 右移
                    chessboard[x1+1][y2] = 0
                    a2, b2 = x1+1, y2
            # 还原前端坐标, 回复报文中(x1,y1)的位置应设置成1，(x2,y2)的位置设置成0
            response['x1'] = a1 + 1
            response['y1'] = b1 + 1
            response['x2'] = a2 + 1
            response['y2'] = b2 + 1 
            print(response)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    response['ifmove'] = move
    return JsonResponse(response)


def checkEnd(request):
    response = {}
    end = True
    for x in range(0, N):
        for y in range(0, N):
            if chessboard[x][y] == 1: # 当前位置有棋子时
                # 判断能否上移
                if y + 2 < N and chessboard[x][y+1] == 1 and chessboard[x][y+2] == 0:
                    end = False
                # 判断能否下移
                if y - 2 >= 0 and chessboard[x][y-1] == 1 and chessboard[x][y-2] == 0:
                    end = False
                # 判断能否右移
                if x + 2 < N and chessboard[x+1][y] == 1 and chessboard[x+2][y] == 0:
                    end = False
                # 判断能否左移
                if x - 2 >= 0 and chessboard[x-1][y] == 1 and chessboard[x-2][y] == 0:
                    end = False
    response['end'] = end
    print(response)
    return JsonResponse(response)

def gethistory(request):
    response = {}
    response['x1'] = x1
    response['y1'] = y1
    response['x2'] = x2
    response['y2'] = y2
    return JsonResponse(response)
