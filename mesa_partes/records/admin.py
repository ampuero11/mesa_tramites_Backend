from django.contrib import admin
from .models import Record, RecordDetail

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "description", "created_by", "created_at")
    search_fields = ("description", "created_by__name")
    list_filter = ("date", "created_at")
    verbose_name = "Acta"
    verbose_name_plural = "Actas"


@admin.register(RecordDetail)
class RecordDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "record", "request", "observation")
    search_fields = ("record__description", "request__code", "request__full_name")
    verbose_name = "Detalle de Acta"
    verbose_name_plural = "Detalles de Acta"
