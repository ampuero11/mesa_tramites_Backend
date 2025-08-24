from django.db import models
from django.contrib.auth.models import AbstractUser
class AdminUser(AbstractUser):
    username = None
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email