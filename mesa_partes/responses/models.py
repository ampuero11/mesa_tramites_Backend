from django.db import models
from requests_app.models import Request
from users.models import AdminUser
import uuid

class Response(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="responses")
    admin = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    message = models.TextField()
    sent_email = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resp. {self.request.code} by {self.admin.email}"
