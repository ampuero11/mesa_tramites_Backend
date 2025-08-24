from rest_framework import serializers
from .models import Record, RecordDetail
from users.serializers import AdminUserSerializer
from requests_app.serializers import RequestSerializer

class RecordDetailSerializer(serializers.ModelSerializer):
    request = RequestSerializer(read_only=True)

    class Meta:
        model = RecordDetail
        fields = ["id", "request", "observation"]

class RecordSerializer(serializers.ModelSerializer):
    created_by = AdminUserSerializer(read_only=True)
    details = RecordDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Record
        fields = ["id", "date", "description", "created_by", "created_at", "details", "file"]
        read_only_fields = ["id", "created_at"]
