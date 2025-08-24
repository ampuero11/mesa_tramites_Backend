from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["id", "original_name", "file_path", "file_type", "size", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]
