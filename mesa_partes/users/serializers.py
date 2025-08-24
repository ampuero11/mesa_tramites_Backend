from rest_framework import serializers
from .models import AdminUser

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ["id", "name", "email", "created_at"]
        read_only_fields = ["id", "created_at"]