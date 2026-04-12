from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    

class Channel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channels')
    name = models.CharField(max_length=100)
    descriptions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Video(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100)
    descriptions = models.TextField()
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.video.title}'
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.video.title}'
    

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='subscribers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} subscribed to {self.channel.name}'