def videos_search(videos, params):
    search = params.get('search')
    if search:
        videos = videos.filter(title__icontains=search)
    return videos


def filter_videos_by_channel(videos, params):
    channel = params.get('channel')
    if channel:
        videos = videos.filter(channel_id=channel)
    return videos


def order_videos(videos, params):
    ordering = params.get('ordering')
    if ordering == 'popular':
        videos = videos.order_by('-views')
    else:
        videos = videos.order_by('-created_at')
    return videos
