from django.conf.urls import url, include
from  playCheseApp.views import *

urlpatterns = [
    url(r'make_size', make_size,),
    url(r'sendPos', sendPos,),
    url(r'index', index,),
    url(r'restart',restart,),
]
