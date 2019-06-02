from django.db import models
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token


@python_2_unicode_compatible
class Device(models.Model):
    serial_number = models.UUIDField()
    firmware_version = models.CharField(max_length=32)
    registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.serial_number)

    def is_alerting(self):
        # Device is alerting in several cases
        # 1. The latest carbon monoxide reading is > 9 PPM
        # 2. The device's latest health status is one of
        #   "needs_service", "needs_new_filter" or "gas_leak."
        latest_co = self.device_sensor_logs.filter(
            sensor_type=DeviceSensorLog.CARBON_MONOXIDE
        ).latest()
        if latest_co.value > 9:
            return True
        bad_statuses = ['needs_service', 'needs_new_filter', 'gas_leak']
        latest_status = self.device_health_status.latest()
        if latest_status.value in bad_statuses:
            return True
        return False


class DeviceToken(Token):
    # Our own version of the Token model where the user is a Device
    user = models.OneToOneField(
        Device, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("Device")
    )


@python_2_unicode_compatible
class DeviceLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-stamp']


@python_2_unicode_compatible
class DeviceSensorLog(DeviceLog):
    TEMPERATURE = 'TM'
    AIR_HUMIDITY = 'HM'
    CARBON_MONOXIDE = 'CO'
    SENSOR_TYPE_CHOICES = [
        (TEMPERATURE, _('Temperature (in Celsius)')),
        (AIR_HUMIDITY, _('Air humidity percentage')),
        (CARBON_MONOXIDE, _('Carbon Monoxide level in the air (PPM)')),
    ]
    sensor_type = models.CharField(
        max_length=2,
        choices=SENSOR_TYPE_CHOICES,
        default=TEMPERATURE,
    )
    value = models.DecimalField(decimal_places=5, max_digits=8)


@python_2_unicode_compatible
class DeviceHealthStatus(DeviceLog):
    value = models.CharField(max_length=150)


@receiver(post_save, sender=Device)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        DeviceToken.objects.create(user=instance)
