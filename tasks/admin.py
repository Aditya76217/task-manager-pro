"""
Admin configuration for Task Manager Pro.
Registers the Task model with a rich admin interface.
"""
from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin view for managing tasks."""
    list_display = ['title', 'priority', 'status', 'assigned_to', 'due_date', 'created_by', 'created_at']
    list_filter = ['priority', 'status', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['priority', 'status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
