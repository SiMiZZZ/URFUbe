from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns =[
    path("", IndexAPIView.as_view()),
    path("upload", UploadAPIView.as_view()),
    path("video/<int:pk>", VideoAPIView.as_view()),
    path("history", HistoryAPIView.as_view()),
    path("comment", CommentAPIView.as_view()),
    path("like", LikeAPIView.as_view()),
    path("dislike", DislikeAPIView.as_view())
]