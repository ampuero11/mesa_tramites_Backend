from django.contrib import admin
from .models import Request, RequestFile, RequestStatus

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "full_name", "document", "status", "created_at")
    search_fields = ("code", "full_name", "document", "email", "phone")
    list_filter = ("status", "created_at")
    verbose_name = "Solicitud"
    verbose_name_plural = "Solicitudes"


@admin.register(RequestFile)
class RequestFileAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "file")
    search_fields = ("request__code", "request__full_name")
    verbose_name = "Archivo de Solicitud"
    verbose_name_plural = "Archivos de Solicitud"


@admin.register(RequestStatus)
class RequestStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "status", "changed_at", "changed_by")
    search_fields = ("request__code", "request__full_name", "changed_by__name")
    list_filter = ("status", "changed_at")
    verbose_name = "Estado de Solicitud"
    verbose_name_plural = "Estados de Solicitud"