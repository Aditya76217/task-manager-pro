"""
Views for Task Manager Pro.

Includes:
- User registration, login, logout
- Dashboard with Kanban board
- Task CRUD (create, read, update, delete)
- AJAX endpoints for drag-and-drop status updates
- Search and filter functionality
"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from .models import Task
from .forms import UserRegisterForm, TaskForm


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Authentication Views
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register_view(request):
    """
    Handle user registration.
    On POST: validate form and create new user, then auto-login.
    On GET: display the registration form.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome aboard, {user.username}! Your account has been created.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    """Log the user out and redirect to login page."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Dashboard View
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@login_required
def dashboard_view(request):
    """
    Main dashboard — displays the Kanban board with three columns.
    Supports filtering by priority, assigned user, and search query.
    Shows tasks the user created OR is assigned to.
    """
    # Base queryset: tasks the user can see
    tasks = Task.objects.filter(
        Q(created_by=request.user) | Q(assigned_to=request.user)
    ).distinct()

    # ── Filters ───────────────────────────────────
    search_query = request.GET.get('search', '').strip()
    priority_filter = request.GET.get('priority', '')
    user_filter = request.GET.get('user', '')

    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    if user_filter:
        tasks = tasks.filter(assigned_to_id=user_filter)

    # ── Split into Kanban columns ─────────────────
    todo_tasks = tasks.filter(status=Task.STATUS_TODO)
    in_progress_tasks = tasks.filter(status=Task.STATUS_IN_PROGRESS)
    done_tasks = tasks.filter(status=Task.STATUS_DONE)

    # ── Progress stats ────────────────────────────
    total = tasks.count()
    done_count = done_tasks.count()
    progress_percent = int((done_count / total) * 100) if total > 0 else 0

    # ── Users for filter dropdown ─────────────────
    all_users = User.objects.filter(is_active=True)

    context = {
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'done_tasks': done_tasks,
        'total_tasks': total,
        'done_count': done_count,
        'progress_percent': progress_percent,
        'search_query': search_query,
        'priority_filter': priority_filter,
        'user_filter': user_filter,
        'all_users': all_users,
        'priority_choices': Task.PRIORITY_CHOICES,
    }
    return render(request, 'tasks/dashboard.html', context)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Task CRUD Views
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@login_required
def task_create_view(request):
    """Create a new task. Automatically sets created_by to the current user."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" created successfully!')
            return redirect('dashboard')
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Create New Task',
        'button_text': 'Create Task',
        'icon': 'bi-plus-circle',
    })


@login_required
def task_edit_view(request, pk):
    """Edit an existing task. Only the creator can edit."""
    task = get_object_or_404(Task, pk=pk)

    # Permission check: only creator or assigned user can edit
    if task.created_by != request.user and task.assigned_to != request.user:
        messages.error(request, 'You do not have permission to edit this task.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated successfully!')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Edit Task',
        'button_text': 'Save Changes',
        'icon': 'bi-pencil-square',
        'task': task,
    })


@login_required
def task_detail_view(request, pk):
    """View full details of a task."""
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_delete_view(request, pk):
    """Delete a task. Only the creator can delete."""
    task = get_object_or_404(Task, pk=pk)

    if task.created_by != request.user:
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('dashboard')

    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted successfully!')
        return redirect('dashboard')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AJAX / API Endpoints
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@login_required
@require_POST
def task_update_status_api(request):
    """
    AJAX endpoint: update a task's status when dragged
    between Kanban columns.
    
    Expects JSON body: { "task_id": int, "new_status": str }
    Returns JSON response with success/error.
    """
    try:
        data = json.loads(request.body)
        task_id = data.get('task_id')
        new_status = data.get('new_status')

        # Validate status
        valid_statuses = [s[0] for s in Task.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return JsonResponse({
                'success': False,
                'error': f'Invalid status: {new_status}'
            }, status=400)

        # Get and update task
        task = get_object_or_404(Task, pk=task_id)

        # Permission check
        if task.created_by != request.user and task.assigned_to != request.user:
            return JsonResponse({
                'success': False,
                'error': 'Permission denied.'
            }, status=403)

        task.status = new_status
        task.save()

        # Calculate new progress
        user_tasks = Task.objects.filter(
            Q(created_by=request.user) | Q(assigned_to=request.user)
        ).distinct()
        total = user_tasks.count()
        done = user_tasks.filter(status=Task.STATUS_DONE).count()
        progress = int((done / total) * 100) if total > 0 else 0

        return JsonResponse({
            'success': True,
            'task_id': task.id,
            'new_status': task.get_status_display(),
            'progress_percent': progress,
            'done_count': done,
            'total_tasks': total,
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def task_stats_api(request):
    """
    AJAX endpoint: return task statistics for the dashboard.
    Used to refresh progress indicators without page reload.
    """
    user_tasks = Task.objects.filter(
        Q(created_by=request.user) | Q(assigned_to=request.user)
    ).distinct()

    total = user_tasks.count()
    todo = user_tasks.filter(status=Task.STATUS_TODO).count()
    in_progress = user_tasks.filter(status=Task.STATUS_IN_PROGRESS).count()
    done = user_tasks.filter(status=Task.STATUS_DONE).count()
    progress = int((done / total) * 100) if total > 0 else 0

    return JsonResponse({
        'total': total,
        'todo': todo,
        'in_progress': in_progress,
        'done': done,
        'progress_percent': progress,
    })
