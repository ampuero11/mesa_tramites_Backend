from django.contrib import admin
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "uploaded_at")
    search_fields = ("file",)
    list_filter = ("uploaded_at",)
    verbose_name = "Archivo"
    verbose_name_plural = "Archivos"