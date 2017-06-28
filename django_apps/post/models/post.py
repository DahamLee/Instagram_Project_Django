from django.conf import settings
from django.db import models

from utils.models.mixin import TimeStampedMixin

__all__ = (
    'Post',
    'PostLike',
)


class Post(TimeStampedMixin):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='post', max_length=30, blank=True)
    video = models.ForeignKey('Video', blank=True, null=True)
    title = models.CharField(max_length=30, blank=True)
    content = models.TextField(max_length=100, blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='like_post',
                                        through='PostLike',
                                        )

    my_comment = models.OneToOneField(
        'Comment',
        blank=True,
        null=True,
        related_name='+')

    class Meta:
        ordering = ['-pk', ]

    def add_comment(self, user, content):
        a = self.comment_set.create(author=user, content=content)
        return a

    @property
    def like_count(self):
        return self.like_users.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     db_table = 'post_post_like_users'
