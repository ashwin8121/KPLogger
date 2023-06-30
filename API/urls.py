from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('get_file', get_text, name="get_text")
]