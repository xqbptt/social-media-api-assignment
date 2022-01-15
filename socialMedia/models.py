from django.db import models
from Authentication.models import User
from django.utils.timezone import now
# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=now)


class Post(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, related_name="posts")
    title = models.TextField(max_length=200)                      
    desc = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=now)
    comments = models.ManyToManyField(Comment, default=[])
    likes = models.ManyToManyField("Authentication.User",blank=True, related_name="likes_list")
