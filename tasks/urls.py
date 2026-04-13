"""
URL patterns for the Tasks app.

Includes authentication routes, dashboard, task CRUD,
and AJAX API endpoints.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ── Authentication ────────────────────────────
    path('', views.dashboard_view, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # ── Task CRUD ─────────────────────────────────
    path('task/new/', views.task_create_view, name='task-create'),
    path('task/<int:pk>/', views.task_detail_view, name='task-detail'),
    path('task/<int:pk>/edit/', views.task_edit_view, name='task-edit'),
    path('task/<int:pk>/delete/', views.task_delete_view, name='task-delete'),

    # ── AJAX API Endpoints ────────────────────────
    path('api/task/update-status/', views.task_update_status_api, name='api-task-update-status'),
    path('api/task/stats/', views.task_stats_api, name='api-task-stats'),
]
