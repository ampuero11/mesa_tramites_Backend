from django.contrib import admin
from .models import AdminUser

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    search_fields = ("name", "email")
    list_filter = ("name",)
    verbose_name = "Administrador"
    verbose_name_plural = "Administradores"
