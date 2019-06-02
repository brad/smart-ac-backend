from django.contrib import admin
from .models import Device, DeviceToken, DeviceSensorLog, DeviceHealthStatus


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(DeviceSensorLog)
class DeviceSensorLogAdmin(admin.ModelAdmin):
    pass


@admin.register(DeviceHealthStatus)
class DeviceHealthStatusAdmin(admin.ModelAdmin):
    pass
