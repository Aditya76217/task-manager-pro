"""
URL configuration for TaskManager Pro project.
Routes all task-related URLs to the tasks app,
and includes Django admin URLs.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),
    # All app URLs (auth + tasks)
    path('', include('tasks.urls')),
]
