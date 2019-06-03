from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Device, DeviceToken, DeviceSensorLog, DeviceHealthStatus


class IsAlertingListFilter(admin.SimpleListFilter):
    title = _('Is alerting?')

    parameter_name = 'is_alerting'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.is_alerting()
        if self.value() == 'No':
            return queryset.not_alerting()


class ReadOnlyInline(admin.TabularInline):
    extra = 0
    readonly_fields = ('stamp',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SensorLogInline(ReadOnlyInline):
    model = DeviceSensorLog


class HealthStatusInline(ReadOnlyInline):
    model = DeviceHealthStatus


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    search_fields = ('serial_number',)
    list_display = ('serial_number', 'registered',)
    list_filter = (IsAlertingListFilter,)
    inlines = [SensorLogInline, HealthStatusInline]


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(DeviceSensorLog)
class DeviceSensorLogAdmin(admin.ModelAdmin):
    list_display = ('sensor_type', 'value', 'device', 'stamp')


@admin.register(DeviceHealthStatus)
class DeviceHealthStatusAdmin(admin.ModelAdmin):
    list_display = ('value', 'device', 'stamp')