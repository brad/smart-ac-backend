from django.contrib import admin
from .models import Device, DeviceToken


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    pass
