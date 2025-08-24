from django.db import models
from files.models import File
from users.models import AdminUser
import uuid

class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    STATUS_CHOICES = [
        ("received", "Recibido"),
        ("in_process", "En Proceso"),
        ("attended", "Atendido"),
        ("rejected", "Rechazado"),
    ]

    code = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=150)
    document = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    concept = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="received")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.full_name}"


class RequestFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="files")
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.request.code} - {self.file.original_name}"


class RequestStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="status_history")
    status = models.CharField(max_length=50)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.request.code} - {self.status}"