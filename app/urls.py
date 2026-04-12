from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListAPIView.as_view()),
    path('users/create/', UserCreateAPIView.as_view()),
    path('users/<int:pk>/', UserDetailAPIView.as_view()),
    path('users/<int:pk>/channels/', UserChannelListAPIView.as_view()),
    path('channels/', ChannelListAPIView.as_view()),
    path('channels/create/', ChannelCreateAPIView.as_view()),
    path('channels/<int:pk>/', ChannelDetailAPIView.as_view()),
    path('channels/<int:pk>/update/', ChannelUpdateAPIView.as_view()),
    path('channels/<int:pk>/delete/', ChannelDeleteAPIView.as_view()),
    path('channels/<int:pk>/videos/', ChannelVideoListAPIView.as_view()),
    path('channels/<int:pk>/stats/', ChannelStatsAPIView.as_view()),
    path('videos/', VideoListAPIView.as_view()),
    path('videos/create/', VideoCreateAPIView.as_view()),
    path('videos/<int:pk>/', VideoDetailAPIView.as_view()),
]
