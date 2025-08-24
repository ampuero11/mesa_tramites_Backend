from django.contrib import admin
from .models import Response

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "admin", "sent_email", "created_at")
    search_fields = ("request__code", "request__full_name", "admin__name")
    list_filter = ("sent_email", "created_at")
    verbose_name = "Respuesta"
    verbose_name_plural = "Respuestas"
