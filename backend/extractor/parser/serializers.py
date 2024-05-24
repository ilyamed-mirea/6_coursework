from rest_framework import serializers


class HTMLSerializer(serializers.Serializer):
    html = serializers.CharField()
