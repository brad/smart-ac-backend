from django.test import TestCase

from faker import Faker
from nose.tools import eq_, ok_

from ..serializers import CreateDeviceSerializer


fake = Faker()

class TestCreateDeviceSerializer(TestCase):

    def setUp(self):
        self.device_data = {
            'serial_number': fake.uuid4(),
            'firmware_version': 'v1.0.0',
        }

    def test_serializer_with_empty_data(self):
        serializer = CreateDeviceSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = CreateDeviceSerializer(data=self.device_data)
        ok_(serializer.is_valid())
