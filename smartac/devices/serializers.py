from rest_framework import serializers

from .models import Device


class CreateDeviceSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # Create the device
        device = Device.objects.create(**validated_data)
        return device

    class Meta:
        model = Device
        fields = ('serial_number', 'firmware_version', 'registered', 'auth_token',)
        read_only_fields = ('auth_token',)
