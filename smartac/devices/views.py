from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from . import serializers
from .models import Device, DeviceSensorLog, DeviceHealthStatus
from .permissions import IsAuthenticated


class DeviceCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Registers devices
    """
    queryset = Device.objects.all()
    serializer_class = serializers.CreateDeviceSerializer
    permission_classes = (AllowAny,)


class DeviceSensorLogCreateViewSet(mixins.CreateModelMixin,
                                   viewsets.GenericViewSet):
    """
    Creates device sensor logs
    """
    queryset = DeviceSensorLog.objects.all()
    serializer_class = serializers.CreateDeviceSensorLogSerializer
    permission_classes = (IsAuthenticated,)


class DeviceHealthStatusCreateViewSet(mixins.CreateModelMixin,
                                      viewsets.GenericViewSet):
    """
    Creates device health status logs
    """
    queryset = DeviceHealthStatus.objects.all()
    serializer_class = serializers.CreateDeviceHealthStatusSerializer
    permission_classes = (IsAuthenticated,)
