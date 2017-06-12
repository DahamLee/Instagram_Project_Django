from django.db import models

from utils.models.mixin import TimeStampedMixin

from django.contrib.auth.models import User


class Post(TimeStampedMixin):
    author = models.ForeignKey(User)
    photo = models.ImageField(max_length=30)

    title = models.CharField(max_length=30)
    content = models.TextField(max_length=100)
    like_users = models.ManyToManyField(User,
                                        related_name='like_post',
                                        through='PostLike',
                                        )
    tags = models.ManyToManyField('Tag')

    def add_comment(self, user, content):
        a = self.comment_set.create(author=user, content=content)
        return a

    def add_tag(self, tag_name):
        tag, tag_created = Tag.objects.get_or_create(name=tag_name)
        if not self.tags.filter(name=tag_name):
            self.tags.add(tag)

    @property
    def like_count(self):
        return self.like_users.count()


class Comment(TimeStampedMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)

    like_users = models.ManyToManyField(
        User,
        through='CommentLike',
        related_name='like_comments'
    )


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     db_table = 'post_post_like_users'


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Tag({})'.format(self.name)

# class User(TimeStampedMixin):
#     name = models.CharField(max_length=30)
