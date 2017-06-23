from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.fields import CustomImageField


class User(AbstractUser):
    nickname = models.CharField(max_length=24, null=True, unique=True)
    img_profile = CustomImageField(
        upload_to='user',
        blank=True,
        # default_static_image='images/profile.png',
    )
    relations = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
    )

    def __str__(self):
        return self.nickname or self.username

    def follow(self, user):
        if not isinstance(user, User):
            raise ValueError('"user" argument must <User> class')
        self.follow_relations.get_or_create(to_user=user)

    def unfollow(self, user):
        self.follow_relations.filter(to_user=user).delete()

    def is_follow(self, user):
        return self.follow_relations.filter(to_user=user).exists()

    def is_follower(self, user):
        return self.follower_relations.filter(from_user=user).exists()

    def follow_toggle(self, user):
        relation, relation_created = self.follow_relations.get_or_create(to_user=user)
        if not relation_created:
            relation.delete()
        else:
            return relation

    @property
    def following(self):
        relations = self.follow_relations.all()
        return User.objects.filter(pk__in=relations.values('to_user'))

    @property
    def followers(self):
        relations = self.follower_relations.all()
        return User.objects.filter(pk__in=relations.values('from_user'))


class Relation(models.Model):
    from_user = models.ForeignKey(User, related_name='follow_relations')
    to_user = models.ForeignKey(User, related_name='follower_relations')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Relation from ({}) ro ({})'.format(self.from_user, self.to_user)

    class Meta:
        unique_together = (
            ('from_user', 'to_user')
        )
