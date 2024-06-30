from django.urls import path
from .views import *

urlpatterns = [
    path('',messageboard,name='messageboard'),
    path('subscribe',subscribe,name='subscribe'),
    path('newsletter',newsletter,name='newsletter'),
]
