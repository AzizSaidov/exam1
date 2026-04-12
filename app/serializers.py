from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    channels_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'created_at', 'channels_count']

    def get_channels_count(self, obj):
        return obj.channels.count()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('Password must be at least 6 characters')
        return value


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'descriptions', 'created_at']


class UserDetailSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True, read_only=True)
    total_videos = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'created_at', 'channels', 'total_videos']

    def get_total_videos(self, obj):
        return Video.objects.filter(channel__owner=obj).count()



class UserChannelSerializer(serializers.ModelSerializer):
    videos_count = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ['id', 'name', 'descriptions', 'created_at', 'videos_count']

    def get_videos_count(self, obj):
        return obj.videos.count()


class ChannelOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ChannelListSerializer(serializers.ModelSerializer):
    owner = ChannelOwnerSerializer(read_only=True)
    subscribers_count = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ['id', 'name', 'descriptions', 'created_at', 'owner', 'subscribers_count']

    def get_subscribers_count(self, obj):
        return obj.subscribers.count()



class ChannelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['owner', 'name', 'descriptions']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('Name cannot be empty')
        return value

    def validate_descriptions(self, value):
        if not value.strip():
            raise serializers.ValidationError('Description cannot be empty')
        return value

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'descriptions', 'views', 'created_at']


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
        total = 0
        for video in obj.videos.all():
            total += video.views
        return total


class ChannelUpdateSerializer(serializers.ModelSerializer):
    updated = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ['id', 'owner', 'name', 'descriptions', 'created_at', 'updated']

    def get_updated(self, obj):
        return True


class ChannelStatsSerializer(serializers.ModelSerializer):
    total_videos = serializers.SerializerMethodField()
    total_views = serializers.SerializerMethodField()
    avg_views = serializers.SerializerMethodField()
    top_video = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ['id', 'name', 'total_videos', 'total_views', 'avg_views', 'top_video']

    def get_total_videos(self, obj):
        return obj.videos.count()

    def get_total_views(self, obj):
        total = 0
        for video in obj.videos.all():
            total += video.views
        return total

    def get_avg_views(self, obj):
        videos = obj.videos.all()
        if videos.count() == 0:
            return 0

        total = 0
        for video in videos:
            total += video.views
        return total / videos.count()

    def get_top_video(self, obj):
        video = obj.videos.order_by('-views').first()
        if video:
            return VideoSerializer(video).data
        return None


class VideoListSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'descriptions', 'views', 'created_at', 'channel']


class VideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['channel', 'title', 'descriptions']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError('Title cannot be empty')
        return value

    def validate_descriptions(self, value):
        if not value.strip():
            raise serializers.ValidationError('Description cannot be empty')
        return value


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
