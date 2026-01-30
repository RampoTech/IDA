from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp', 'is_admin_reply')
    list_filter = ('user', 'is_admin_reply', 'timestamp')
