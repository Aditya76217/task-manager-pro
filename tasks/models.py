"""
Models for Task Manager Pro.

Task model stores all task information including title, description,
priority, status, due date, and user assignments for collaboration.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    """
    Represents a single task in the kanban board.
    
    Each task has a title, description, priority level, status,
    due date, creator, and optionally an assigned user for
    team collaboration.
    """

    # ── Priority choices ──────────────────────────
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    ]

    # ── Status choices (Kanban columns) ───────────
    STATUS_TODO = 'todo'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_CHOICES = [
        (STATUS_TODO, 'To Do'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_DONE, 'Done'),
    ]

    # ── Fields ────────────────────────────────────
    title = models.CharField(
        max_length=200,
        help_text="Short, descriptive title for the task."
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text="Detailed description of what needs to be done."
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM,
        help_text="Urgency level of the task."
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_TODO,
        help_text="Current stage in the workflow."
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="Deadline for the task."
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        help_text="User who created this task."
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        help_text="User responsible for completing this task."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        """Check if the task is past its due date and not yet done."""
        if self.due_date and self.status != self.STATUS_DONE:
            return self.due_date < timezone.now().date()
        return False

    @property
    def priority_color(self):
        """Return a Bootstrap color class based on priority."""
        colors = {
            self.PRIORITY_LOW: 'success',      # Green
            self.PRIORITY_MEDIUM: 'warning',    # Yellow/Orange
            self.PRIORITY_HIGH: 'danger',       # Red
        }
        return colors.get(self.priority, 'secondary')

    @property
    def priority_icon(self):
        """Return an icon class based on priority."""
        icons = {
            self.PRIORITY_LOW: 'bi-arrow-down',
            self.PRIORITY_MEDIUM: 'bi-dash',
            self.PRIORITY_HIGH: 'bi-arrow-up',
        }
        return icons.get(self.priority, 'bi-dash')
