from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Count
from django.db.models.functions import Length
from drf_yasg.utils import swagger_auto_schema

from .models import *
from .serializers import *
from .paginations import *
from .filters import *




class RegisterAPIView(APIView):
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: "Created", 400: "Validation error"}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    @swagger_auto_schema(
        responses={200: "OK", 400: "Validation error"}
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=HTTP_200_OK)

        return Response(
            {"error": "Invalid credentials"},
            status=HTTP_400_BAD_REQUEST
        )


class ProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"user": request.user.username})














#1
class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    pagination_class = UserListPagination

    def get_queryset(self):
        return User.objects.annotate(channels_count=Count('channels'))


#2
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


#3
class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


#4
class UserChannelListAPIView(ListAPIView):
    serializer_class = UserChannelSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Channel.objects.filter(owner_id=pk)


#5
class ChannelListAPIView(ListAPIView):
    serializer_class = ChannelListSerializer

    def get_queryset(self):
        return Channel.objects.annotate(subscribers_count=Count('subscribers'))


#6
class ChannelCreateAPIView(CreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelCreateSerializer


#7
class ChannelDetailAPIView(RetrieveAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelDetailSerializer


#8
class ChannelUpdateAPIView(UpdateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelUpdateSerializer


#9
class ChannelDeleteAPIView(DestroyAPIView):
    queryset = Channel.objects.all()

    def destroy(self, request, *args, **kwargs):
        channel = self.get_object()
        deleted_channel_id = channel.id
        channel.delete()

        return Response(
            {
                'status': 'deleted',
                'deleted_channel_id': deleted_channel_id
            },
            status=HTTP_200_OK
        )


#10
class ChannelVideoListAPIView(ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Video.objects.filter(channel_id=pk)
        return filter_channel_videos(self.request, queryset)


#11
class ChannelStatsAPIView(RetrieveAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelStatsSerializer


#12, #25
class VideoListAPIView(ListAPIView):
    serializer_class = VideoListSerializer
    pagination_class = VideoListPagination

    def get_queryset(self):
        queryset = Video.objects.all()
        queryset = filter_videos(self.request, queryset)
        return filter_videos_by_channel(self.request, queryset)


#13
class VideoCreateAPIView(CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoCreateSerializer


#14
class VideoDetailAPIView(RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        video = self.get_object()
        video.views += 1
        video.save()

        serializer = self.get_serializer(video)
        return Response(serializer.data, status=HTTP_200_OK)


#15
class VideoUpdateAPIView(UpdateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoUpdateSerializer


#16
class VideoDeleteAPIView(DestroyAPIView):
    queryset = Video.objects.all()

    def destroy(self, request, *args, **kwargs):
        video = self.get_object()
        deleted_video_id = video.id
        deleted_comments_count = video.comments.count()
        deleted_likes_count = video.likes.count()

        video.delete()

        return Response(
            {
                'status': 'deleted',
                'deleted_video_id': deleted_video_id,
                'deleted_comments_count': deleted_comments_count,
                'deleted_likes_count': deleted_likes_count,
            },
            status=HTTP_200_OK
        )


#17
class VideoCommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CommentListPagination

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Comment.objects.filter(video_id=pk)
        sort = self.request.GET.get('sort')

        if sort == 'old':
            return queryset.order_by('created_at')

        if sort == 'popular':
            return queryset.annotate(text_length=Length('text')).order_by('-text_length', '-created_at')

        return queryset.order_by('-created_at')


#18
class VideoCommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        video_id = self.kwargs.get('pk')

        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            raise ValidationError({'video': 'Video not found'})

        serializer.save(video=video)


#19
class CommentDetailAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer


#20
class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        deleted_comment_id = comment.id
        comment.delete()

        return Response(
            {
                'status': 'deleted',
                'deleted_comment_id': deleted_comment_id
            },
            status=HTTP_200_OK
        )


#21
class VideoLikeCreateAPIView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = LikeCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        video_id = self.kwargs.get('pk')
        user_id = serializer.validated_data['user_id']

        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found'}, status=HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=HTTP_404_NOT_FOUND)

        if Like.objects.filter(user=user, video=video).exists():
            return Response({'error': 'Like already exists'}, status=HTTP_400_BAD_REQUEST)

        Like.objects.create(user=user, video=video)

        return Response(
            {
                'liked': True,
                'total_likes': video.likes.count()
            },
            status=HTTP_201_CREATED
        )


#22
class VideoLikeDeleteAPIView(DestroyAPIView):
    queryset = Like.objects.all()

    def destroy(self, request, *args, **kwargs):
        video_id = self.kwargs.get('pk')
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'error': 'user_id is required'}, status=HTTP_400_BAD_REQUEST)

        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found'}, status=HTTP_404_NOT_FOUND)

        try:
            like = Like.objects.get(video_id=video_id, user_id=user_id)
        except Like.DoesNotExist:
            return Response({'error': 'Like not found'}, status=HTTP_404_NOT_FOUND)

        like.delete()

        return Response(
            {
                'liked': False,
                'total_likes': video.likes.count()
            },
            status=HTTP_200_OK
        )


#23
class VideoLikeListAPIView(ListAPIView):
    serializer_class = LikeUserSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return User.objects.filter(likes__video_id=pk)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'users': serializer.data,
                'total_count': queryset.count()
            },
            status=HTTP_200_OK
        )


#24
class VideoSearchAPIView(ListAPIView):
    serializer_class = VideoListSerializer

    def get_queryset(self):
        queryset = Video.objects.all()
        return search_videos(self.request, queryset)