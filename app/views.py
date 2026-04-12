from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from .filters import *
from .models import *
from .serializers import *
from .paginations import *


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserListPagination


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserChannelListAPIView(ListAPIView):
    serializer_class = UserChannelSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Channel.objects.filter(owner_id=pk)


class ChannelListAPIView(ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelListSerializer



class ChannelCreateAPIView(CreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelCreateSerializer



class ChannelDetailAPIView(RetrieveAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelDetailSerializer



class ChannelUpdateAPIView(UpdateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelUpdateSerializer


class ChannelDeleteAPIView(DestroyAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelDetailSerializer


class ChannelVideoListAPIView(ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Video.objects.filter(channel_id=pk)


class ChannelStatsAPIView(RetrieveAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelStatsSerializer


class VideoListAPIView(ListAPIView):
    serializer_class = VideoListSerializer
    pagination_class = VideoListPagination

    def get_queryset(self):
        videos = Video.objects.all()
        videos = videos_search(videos, self.request.GET)
        videos = filter_videos_by_channel(videos, self.request.GET)
        videos = order_videos(videos, self.request.GET)
        return videos


class VideoCreateAPIView(CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoCreateSerializer


class VideoDetailAPIView(RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer

    def get_object(self):
        video = super().get_object()
        video.views += 1
        video.save()
        return video
