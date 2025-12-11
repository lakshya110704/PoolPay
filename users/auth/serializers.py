from rest_framework import serializers

class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=32)

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=32)
    code = serializers.CharField(max_length=6)