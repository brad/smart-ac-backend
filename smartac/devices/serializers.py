from rest_framework import serializers

from .models import Device, DeviceSensorLog, DeviceHealthStatus


class CreateDeviceSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # Create the device
        device = Device.objects.create(**validated_data)
        return device

    class Meta:
        model = Device
        fields = (
            'id',
            'serial_number',
            'firmware_version',
            'registered',
            'auth_token',
        )
        read_only_fields = ('id', 'auth_token',)


class CreateDeviceSensorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceSensorLog
        fields = ('sensor_type', 'stamp', 'value')
        read_only_fields = ('stamp',)


class CreateDeviceHealthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceHealthStatus
        fields = ('stamp', 'value')
        read_only_fields = ('stamp',)
