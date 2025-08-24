from django.contrib import admin
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_name', 'file_path', 'file_type', 'size', 'uploaded_at')
    search_fields = ('original_name', 'file_type')
    list_filter = ('file_type', 'uploaded_at')
    verbose_name = "Archivo"
    verbose_name_plural = "Archivos"