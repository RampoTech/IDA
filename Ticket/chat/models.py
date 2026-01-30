from django.db import models
from django.conf import settings

class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_admin_reply = models.BooleanField(default=False)
    # session_id can be added if we support guest chat, but requirement says "Get User info from DB" so assuming auth users.

    def __str__(self):
        return f"{self.user} - {self.timestamp}: {self.message[:20]}"
