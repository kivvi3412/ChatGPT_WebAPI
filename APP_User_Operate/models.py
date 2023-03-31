import uuid
from django.db import models
from APP_Users_Login.models import UserInfo


# Create your models here.
class ChatInfo(models.Model):
    chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="chat_id")
    user_id = models.IntegerField(help_text="user_id")
    openai_params = models.JSONField(help_text="openai_params")
    chat_summary = models.CharField(max_length=200, help_text="chat_summary")
    chat_message = models.JSONField(help_text="chat_message")
    is_deleted = models.BooleanField(default=False, help_text="is_deleted")
    updated_at = models.DateTimeField(auto_now=True, help_text="updated_at")
