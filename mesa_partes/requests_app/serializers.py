from rest_framework import serializers
from .models import Request, RequestFile, RequestStatus
from files.serializers import FileSerializer
from users.serializers import AdminUserSerializer

class RequestFileSerializer(serializers.ModelSerializer):
    file = FileSerializer(read_only=True)

    class Meta:
        model = RequestFile
        fields = ["id", "file"]

class RequestStatusSerializer(serializers.ModelSerializer):
    changed_by = AdminUserSerializer(read_only=True)

    class Meta:
        model = RequestStatus
        fields = ["id", "status", "changed_at", "changed_by"]

class RequestSerializer(serializers.ModelSerializer):
    files = RequestFileSerializer(many=True, read_only=True)
    status_history = RequestStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Request
        fields = [
            "id", "code", "full_name", "document", "email", "phone",
            "concept", "status", "created_at", "files", "status_history"
        ]
        read_only_fields = ["id", "created_at"]
