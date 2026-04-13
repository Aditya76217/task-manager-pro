from django.apps import AppConfig


class TasksConfig(AppConfig):
    """Configuration for the Tasks application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    verbose_name = 'Task Manager'
