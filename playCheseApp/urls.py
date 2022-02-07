from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'make_size', views.make_size,),
    url(r'getpiecearray', views.get_piece_array,),
    url(r'restart',views.restart,),
    url(r'sendpos',views.sendPos,),
    url(r'checkend',views.checkEnd,)
]
