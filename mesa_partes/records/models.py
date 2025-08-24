from django.db import models
from requests_app.models import Request
from users.models import AdminUser

class Record(models.Model):
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Acta {self.date}"


class RecordDetail(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name="details")
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    observation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.record.date} - {self.request.code}"
