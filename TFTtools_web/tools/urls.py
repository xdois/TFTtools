from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('augment', views.augments, name='augment'),
    path('champion', views.champions, name='champion'),
    path('item', views.items, name='item'),
    path('trait', views.traits, name='trait'),
]
