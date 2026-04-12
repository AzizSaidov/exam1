from django.contrib import admin
from .models import User, Channel, Video, Comment, Like, Subscription

admin.site.register(User)
admin.site.register(Channel)
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Subscription)