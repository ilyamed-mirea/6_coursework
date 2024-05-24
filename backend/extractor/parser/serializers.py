from rest_framework import serializers


class HTMLSerializer(serializers.Serializer):
    html = serializers.CharField()


class ReplaceTextSerializer(serializers.Serializer):
    html = serializers.CharField()
    old_text = serializers.CharField()
    new_text = serializers.CharField()
