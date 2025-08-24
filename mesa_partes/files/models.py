from django.db import models
import uuid

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    original_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to="uploads/")
    file_type = models.CharField(max_length=50, default='pdf')
    size = models.PositiveIntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name