import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, Group
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from allauth.account import signals as allauth_signals


@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(allauth_signals.user_signed_up)
def user_signed_up(request, user, **kwargs):
    # Enable the user to use admin
    user.is_staff = True
    user.save()
    # Add the user to the Staff group
    Group.objects.get(name='Staff').user_set.add(user)
