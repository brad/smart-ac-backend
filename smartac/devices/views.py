from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers
from .models import Device, DeviceSensorLog, DeviceHealthStatus
from .permissions import IsAuthenticated


class DeviceCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Registers devices
    """
    queryset = Device.objects.none()
    serializer_class = serializers.CreateDeviceSerializer
    permission_classes = (AllowAny,)


class DeviceLogCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    # A viewset for device logs that allows creating one or multiple objects
    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)

    def perform_create(self, serializer):
        if type(serializer.validated_data) == list:
            for item in serializer.validated_data:
                item.update({'device': self.request.user})
        else:
            serializer.validated_data.update({'device': self.request.user})
        serializer.save()


class DeviceSensorLogCreateViewSet(DeviceLogCreateViewSet):
    """
    Creates device sensor logs
    """
    queryset = DeviceSensorLog.objects.none()
    serializer_class = serializers.CreateDeviceSensorLogSerializer
    permission_classes = (IsAuthenticated,)


class DeviceHealthStatusCreateViewSet(DeviceLogCreateViewSet):
    """
    Creates device health status logs
    """
    queryset = DeviceHealthStatus.objects.none()
    serializer_class = serializers.CreateDeviceHealthStatusSerializer
    permission_classes = (IsAuthenticated,)
