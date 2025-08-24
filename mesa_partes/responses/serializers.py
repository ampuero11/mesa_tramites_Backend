from rest_framework import serializers
from .models import Response
from users.serializers import AdminUserSerializer

class ResponseSerializer(serializers.ModelSerializer):
    admin = AdminUserSerializer(read_only=True)

    class Meta:
        model = Response
        fields = ["id", "request", "admin", "message", "sent_email", "created_at"]
        read_only_fields = ["id", "created_at"]
