from django.contrib import admin
from django.utils.translation import gettext_lazy as _

import pygal

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
    change_form_template = 'devices/change_form.html'

    def get_sensor_chart(self):
        chart = pygal.Line(disable_xml_declaration=True)
        chart.title = 'Sensor Logs for Today'
        chart.x_labels = map(str, range(0, 24))
        # TODO: Use real data!
        # Temperature
        chart.add(str(DeviceSensorLog.SENSOR_TYPE_CHOICES[0][1]), [
            10, 10, 11, 11.5, 12, 12.5, 12.75, 13, 13.5, 13.75, 14, 15,
            15.6, 16, 17, 16, 15, 14.5, 14, 13.5, 13, 12, 11, 10.5,
        ])
        # Humidity
        chart.add(str(DeviceSensorLog.SENSOR_TYPE_CHOICES[1][1]), [
            67, 66, 63, 64, 55, 50, 57, 45, 40, 60, 35, 30,
            35, 25, 45, 40, 42, 43, 42, 55, 60, 58, 65, 70
        ])
        # Carbon Monoxide
        chart.add(str(DeviceSensorLog.SENSOR_TYPE_CHOICES[2][1]), [
            0, 0, 1, 0.56, 0.567, 1, 2, 3, 4, 5, 6, 7,
            8, 9, 10, 8, 9, 5, 2, 0, 0, 0, 0, 0
        ])
        return chart.render()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['sensor_chart'] = self.get_sensor_chart()
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(DeviceSensorLog)
class DeviceSensorLogAdmin(admin.ModelAdmin):
    list_display = ('sensor_type', 'value', 'device', 'stamp')


@admin.register(DeviceHealthStatus)
class DeviceHealthStatusAdmin(admin.ModelAdmin):
    list_display = ('value', 'device', 'stamp')
