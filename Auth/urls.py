from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns =[
    path("register", RegisterAPIView.as_view()),
    path("render_register", register_user_render),
    path("logout", LogoutAPIView.as_view()),
    path("login", LoginAPIView.as_view())
]