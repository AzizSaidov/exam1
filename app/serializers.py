from rest_framework import serializers
from django.db.models import Sum, Avg, Count
from .models import *



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user











#1
class UserSerializer(serializers.ModelSerializer):
    channels_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at', 'channels_count']

#2
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


####
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'descriptions', 'created_at']


#3
class UserDetailSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True, read_only=True)
    total_videos = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at', 'channels', 'total_videos']

    def get_total_videos(self, obj):
        return Video.objects.filter(channel__owner=obj).count()


#4
class UserChannelSerializer(serializers.ModelSerializer):
    videos_count = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ['id', 'name', 'descriptions', 'created_at', 'videos_count']

    def get_videos_count(self, obj):
        return obj.videos.count()


####
class ChannelOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


#5
class ChannelListSerializer(serializers.ModelSerializer):
    owner = ChannelOwnerSerializer(read_only=True)
    subscribers_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Channel
        fields = ['id', 'name', 'descriptions', 'created_at', 'owner', 'subscribers_count']

#6
class ChannelCreateSerializer(serializers.ModelSerializer):
    owner = ChannelOwnerSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='owner'
    )
    total_videos = serializers.SerializerMethodField()
    total_views = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ['id', 'owner', 'owner_id', 'name', 'descriptions', 'created_at', 'total_videos', 'total_views']
        read_only_fields = ['id', 'created_at']

    def get_total_videos(self, obj):
        return obj.videos.count()

    def get_total_views(self, obj):
        return obj.videos.aggregate(total_views=Sum('views'))['total_views'] or 0


#####
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'descriptions', 'views', 'created_at']


#7
class ChannelDetailSerializer(serializers.ModelSerializer):
    owner = ChannelOwnerSerializer(read_only=True)
    latest_videos = serializers.SerializerMethodField()
    total_views = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ['id', 'name', 'descriptions', 'created_at', 'owner', 'latest_videos', 'total_views']

    def get_latest_videos(self, obj):
        videos = obj.videos.all().order_by('-created_at')[:5]
        return VideoSerializer(videos, many=True).data

    def get_total_views(self, obj):
        return obj.videos.aggregate(total_views=Sum('views'))['total_views'] or 0


#8
class ChannelUpdateSerializer(serializers.ModelSerializer):
    owner = ChannelOwnerSerializer(read_only=True)
    updated = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ['id', 'owner', 'name', 'descriptions', 'created_at', 'updated']

    def get_updated(self, obj):
        return True


#11
class ChannelStatsSerializer(serializers.ModelSerializer):
    total_videos = serializers.SerializerMethodField()
    total_views = serializers.SerializerMethodField()
    avg_views = serializers.SerializerMethodField()
    top_video = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ['id', 'name', 'total_videos', 'total_views', 'avg_views', 'top_video']

    def get_total_videos(self, obj):
        return obj.videos.aggregate(total_videos=Count('id'))['total_videos'] or 0

    def get_total_views(self, obj):
        return obj.videos.aggregate(total_views=Sum('views'))['total_views'] or 0

    def get_avg_views(self, obj):
        avg_views = obj.videos.aggregate(avg_views=Avg('views'))['avg_views']
        if avg_views is None:   
            return 0
        return avg_views

    def get_top_video(self, obj):
        video = obj.videos.order_by('-views').first()
        if video:
            return VideoSerializer(video).data
        return None


#12
class VideoListSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'descriptions', 'views', 'created_at', 'channel']


#13
class VideoCreateSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True)
    channel_id = serializers.PrimaryKeyRelatedField(
        queryset=Channel.objects.all(),
        write_only=True,
        source='channel'
    )

    class Meta:
        model = Video
        fields = ['id', 'channel', 'channel_id', 'title', 'descriptions', 'views', 'created_at']
        read_only_fields = ['id', 'views', 'created_at']


#14
class VideoDetailSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'descriptions', 'views', 'created_at', 'channel', 'comments_count', 'likes_count']

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.likes.count()


#15
class VideoUpdateSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True)
    channel_id = serializers.PrimaryKeyRelatedField(
        queryset=Channel.objects.all(),
        write_only=True,
        source='channel'
    )

    class Meta:
        model = Video
        fields = ['id', 'channel', 'channel_id', 'title', 'descriptions', 'views', 'created_at']
        read_only_fields = ['id', 'views', 'created_at']


######
class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


#17
class CommentListSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'user']


#18
class CommentCreateSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='user'
    )
    video_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'user', 'user_id', 'video_id']
        read_only_fields = ['id', 'created_at']


#19
class CommentDetailSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer(read_only=True)
    video = VideoSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'user', 'video']


#21
class LikeCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Like
        fields = ['user_id']


#23
class LikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
