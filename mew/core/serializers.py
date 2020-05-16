import time
from rest_framework import serializers


class SerializedDateTimeField(serializers.Field):
    """
        This will help in serializing the Django Model `DateTimeField` into
        a proper format that can be used across applications.
    """
    def to_representation(self, value):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    def to_internal_value(self, value):
        pass


class SerializedTimeStampField(serializers.Field):
    """
        This will help in serializing the Django Model `DateTimeField` into
        a proper format that can be used across applications.
    """
    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))

    def to_internal_value(self, value):
        pass
