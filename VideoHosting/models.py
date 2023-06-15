from django.db import models
from django.conf import settings


class Video(models.Model):
    name = models.CharField(max_length=30, default="Название")
    url = models.TextField(max_length=200, default="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    preview_url = models.TextField(max_length=200,
                                   default="https://urfube.hb.ru-msk.vkcs.cloud/71672490903876c42ea496da39ac6220.png")
    cloud_name = models.TextField(max_length=300, null=True)

    class Meta:
        ordering = ["-id"]


class Reaction(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)


class Comment(models.Model):
    text = models.TextField(max_length=300, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]


class History(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-id"]


class Subscription(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author")
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriber")
