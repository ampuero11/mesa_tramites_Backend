from rest_framework import serializers
from .models import Request, RequestFile, RequestStatus
from files.serializers import FileSerializer
from users.serializers import AdminUserSerializer
from files.models import File
from mesa_partes.utils.response import custom_response
from django.utils import timezone

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

class RequestCreateSerializer(serializers.ModelSerializer):
    uploaded_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=True
    )

    class Meta:
        model = Request
        fields = ["full_name", "document", "email", "phone", "concept", "uploaded_files"]

    from django.utils import timezone

    def create(self, validated_data):
        files_data = validated_data.pop("uploaded_files", [])

        last_request = Request.objects.order_by("-created_at").first()
        next_number = (last_request.code_number + 1) if last_request else 1

        validated_data["code"] = f"TRM-{timezone.now().year}-{next_number:04d}"

        request_instance = Request.objects.create(**validated_data)

        for f in files_data:
            file_instance = File.objects.create(
                original_name=f.name,
                file_path=f,
                file_type=f.name.split(".")[-1].lower(),
                size=f.size
            )
            RequestFile.objects.create(request=request_instance, file=file_instance)

        return request_instance