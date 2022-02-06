from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
import numpy as np

from .models import Size

@require_http_methods(["GET"])
def make_size(request):
    response = {}
    size = Size(size=5)
    try:
        t = int(request.GET.get('size'))
        size = Size(size=t)
        response['size'] = str(t)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

@require_http_methods(["GET"])
def get_piece_array(request):
    arr = np.ones((15,15))
    return JsonResponse(arr.tolist(), safe=False)

@require_http_methods(["GET"])
def restart(request):
    response = {}
    try:
        response['error_num'] = 0
        response['msg'] = 'success'
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
