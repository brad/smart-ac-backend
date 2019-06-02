from django.db import models
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token


@python_2_unicode_compatible
class Device(models.Model):
    serial_number = models.UUIDField()
    registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.serial_number)


class DeviceToken(Token):
    # Our own version of the Token model where the user is a Device
    user = models.OneToOneField(
        Device, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("Device")
    )


@receiver(post_save, sender=Device)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        DeviceToken.objects.create(user=instance)
