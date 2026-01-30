from django.contrib import admin
from .models import Ticket, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'description')
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'author', 'created_at')
