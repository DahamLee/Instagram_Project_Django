from django.db import models

from utils.models.mixin import TimeStampedMixin


class Post(TimeStampedMixin):
    # author, user 필드는 제외하고 생성
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=100)
    like_users = models.ManyToManyField('User',
                                        through='PostLike',
                                        )
    tags = models.ManyToManyField('Tag')


class Comment(TimeStampedMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField(max_length=100)


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('User')
    created_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    title = models.CharField(max_length=50)


class User(TimeStampedMixin):
    name = models.CharField(max_length=30)
