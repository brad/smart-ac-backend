from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token


class LogsQuerySet(models.QuerySet):
    bad_statuses = ['needs_service', 'needs_new_filter', 'gas_leak']

    def latest_annotations(self):
        # Device is alerting in several cases
        # 1. The latest carbon monoxide reading is > 9 PPM
        # 2. The device's latest health status is one of
        #   "needs_service", "needs_new_filter" or "gas_leak."
        latest_co = models.Subquery(DeviceSensorLog.objects.filter(
            device=models.OuterRef('pk'),
            sensor_type=DeviceSensorLog.CARBON_MONOXIDE
        ).order_by('-stamp').values('value')[:1])
        latest_status = models.Subquery(DeviceHealthStatus.objects.filter(
            device=models.OuterRef('pk'),
        ).order_by('-stamp').values('value')[:1])
        return self.annotate(
            latest_co=latest_co,
            latest_status=latest_status
        )

    def is_alerting(self):
        return self.latest_annotations().filter(
            Q(latest_co__gt=9) | Q(latest_status__in=self.bad_statuses))

    def not_alerting(self):
        return self.exclude(id__in=self.is_alerting().values('id'))


class LogsManager(models.Manager):
    def get_queryset(self):
        return LogsQuerySet(self.model, using=self._db)

    def is_alerting(self):
        return self.get_queryset().is_alerting()

    def not_alerting(self):
        return self.get_queryset().not_alerting()


@python_2_unicode_compatible
class Device(models.Model):
    serial_number = models.UUIDField()
    firmware_version = models.CharField(max_length=32)
    registered = models.DateTimeField(auto_now_add=True)

    logs = LogsManager()
    objects = models.Manager()

    def __str__(self):
        return str(self.serial_number)


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
