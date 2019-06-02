from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from .models import Device
from .serializers import CreateDeviceSerializer


class DeviceCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Registers devices
    """
    queryset = Device.objects.all()
    serializer_class = CreateDeviceSerializer
    permission_classes = (AllowAny,)
