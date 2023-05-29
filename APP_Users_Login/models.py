from django.db import models
from django.utils import timezone


# Create your models here.
class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True, help_text="user_id")
    username = models.CharField(max_length=30, unique=True, help_text="username")
    password = models.CharField(max_length=200, blank=True, help_text="password")
    avatar_link = models.CharField(max_length=200, blank=True, null=True, help_text="avatar_link")
    is_active = models.BooleanField(default=True, help_text="is_active")
    is_staff = models.BooleanField(default=False, help_text="is_staff")
    date_joined = models.DateTimeField(default=timezone.now, help_text="date_joined")
    last_login = models.DateTimeField(null=True, blank=True, help_text="last_login")
    token = models.CharField(max_length=200, blank=True, null=True, help_text="token")
