from django.contrib import admin
from .models import AdminUser

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "created_at")
    search_fields = ("name", "email")
    list_filter = ("created_at",)
    verbose_name = "Administrador"
    verbose_name_plural = "Administradores"
