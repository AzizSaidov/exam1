def filter_channel_videos(request, queryset):
    sort = request.GET.get('sort')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        queryset = queryset.filter(created_at__date__gte=start_date)

    if end_date:
        queryset = queryset.filter(created_at__date__lte=end_date)

    if sort == 'popular':
        queryset = queryset.order_by('-views')
    else:
        queryset = queryset.order_by('-created_at')

    return queryset


#12
def filter_videos(request, queryset):
    query = request.GET.get('query')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    ordering = request.GET.get('ordering')

    if query:
        title_queryset = queryset.filter(title__icontains=query)
        description_queryset = queryset.filter(descriptions__icontains=query)
        queryset = title_queryset | description_queryset

    if start_date:
        queryset = queryset.filter(created_at__date__gte=start_date)

    if end_date:
        queryset = queryset.filter(created_at__date__lte=end_date)

    if ordering == 'popular':
        queryset = queryset.order_by('-views')
    elif ordering == 'oldest':
        queryset = queryset.order_by('created_at')
    else:
        queryset = queryset.order_by('-created_at')

    return queryset


#25
def filter_videos_by_channel(request, queryset):
    channel_id = request.GET.get('channel')

    if not channel_id:
        return queryset

    queryset = queryset.filter(channel_id=channel_id)
    return queryset.order_by('-views')


#24
def search_videos(request, queryset):
    query = request.GET.get('query')

    if not query:
        return queryset.none()

    title_queryset = queryset.filter(title__icontains=query)
    description_queryset = queryset.filter(descriptions__icontains=query)
    return title_queryset | description_queryset
