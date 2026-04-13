"""
Quick setup script for TaskManager Pro.

Run this script to:
1. Make migrations
2. Apply migrations
3. Create demo users (separate from Django admin)
4. Seed sample task data
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User


def setup():
    """Run all setup steps."""
    print("=" * 60)
    print("  TaskManager Pro — Quick Setup")
    print("=" * 60)

    # Step 1: Make migrations
    print("\n[1/5] Making migrations...")
    call_command('makemigrations', 'tasks')
    print("     ✓ Migrations created")

    # Step 2: Apply migrations
    print("\n[2/5] Applying migrations...")
    call_command('migrate')
    print("     ✓ Database ready")

    # Step 3: Create Django admin superuser (separate)
    print("\n[3/5] Creating Django admin superuser...")
    if not User.objects.filter(username='superadmin').exists():
        User.objects.create_superuser(
            username='superadmin',
            email='superadmin@taskmanager.com',
            password='superadmin123'
        )
        print("     ✓ Django Admin: superadmin / superadmin123")
        print("       (Access at /admin — NOT for regular app login)")
    else:
        print("     → Superuser 'superadmin' already exists")

    # Step 4: Create regular app users
    print("\n[4/5] Creating regular app users...")
    create_app_users()

    # Step 5: Create sample tasks
    print("\n[5/5] Seeding sample tasks...")
    create_sample_data()

    print("\n" + "=" * 60)
    print("  ✅  Setup complete!")
    print("=" * 60)
    print("\n  Run the server with:")
    print("    python manage.py runserver")
    print("\n  Then open: http://127.0.0.1:8000")
    print("\n  ┌──────────────────────────────────────────┐")
    print("  │  APP LOGIN ACCOUNTS:                     │")
    print("  │  • john    / john1234                     │")
    print("  │  • alice   / alice1234                    │")
    print("  │  • bob     / bob12345                     │")
    print("  │                                           │")
    print("  │  DJANGO ADMIN (separate, /admin only):    │")
    print("  │  • superadmin / superadmin123              │")
    print("  └──────────────────────────────────────────┘")
    print("=" * 60)


def create_app_users():
    """
    Create regular application users.
    These are separate from Django admin superuser.
    """
    app_users = [
        ('john', 'john@example.com', 'John', 'Doe', 'john1234'),
        ('alice', 'alice@example.com', 'Alice', 'Smith', 'alice1234'),
        ('bob', 'bob@example.com', 'Bob', 'Johnson', 'bob12345'),
    ]

    for username, email, first, last, password in app_users:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first,
                'last_name': last,
                'is_staff': False,       # NOT a staff user
                'is_superuser': False,   # NOT a superuser
            }
        )
        if created:
            user.set_password(password)
            user.save()
            print(f"     ✓ User '{username}' created (password: {password})")
        else:
            print(f"     → User '{username}' already exists")


def create_sample_data():
    """Create sample tasks for demo purposes."""
    from tasks.models import Task
    from datetime import date, timedelta

    # Skip if tasks already exist
    if Task.objects.exists():
        print("     → Sample tasks already exist, skipping")
        return

    # Get the regular app users
    try:
        john = User.objects.get(username='john')
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
    except User.DoesNotExist:
        print("     ✗ Could not find users. Run create_app_users() first.")
        return

    # Create sample tasks
    today = date.today()
    sample_tasks = [
        {
            'title': 'Design landing page mockup',
            'description': 'Create a high-fidelity mockup for the new landing page using Figma. Include hero section, features, and pricing.',
            'priority': 'high',
            'status': 'todo',
            'due_date': today + timedelta(days=3),
            'created_by': john,
            'assigned_to': alice,
        },
        {
            'title': 'Set up CI/CD pipeline',
            'description': 'Configure GitHub Actions for automated testing and deployment to staging environment.',
            'priority': 'high',
            'status': 'in_progress',
            'due_date': today + timedelta(days=5),
            'created_by': john,
            'assigned_to': bob,
        },
        {
            'title': 'Write API documentation',
            'description': 'Document all REST API endpoints with request/response examples using Swagger/OpenAPI specification.',
            'priority': 'medium',
            'status': 'todo',
            'due_date': today + timedelta(days=7),
            'created_by': john,
            'assigned_to': john,
        },
        {
            'title': 'Fix login page responsive issues',
            'description': 'The login form breaks on mobile devices below 375px width. Fix CSS grid layout.',
            'priority': 'medium',
            'status': 'in_progress',
            'due_date': today + timedelta(days=2),
            'created_by': alice,
            'assigned_to': john,
        },
        {
            'title': 'Database backup automation',
            'description': 'Set up automated daily backups for the production database using cron jobs.',
            'priority': 'high',
            'status': 'done',
            'due_date': today - timedelta(days=1),
            'created_by': john,
            'assigned_to': bob,
        },
        {
            'title': 'Update dependencies',
            'description': 'Review and update all npm and pip packages to their latest stable versions.',
            'priority': 'low',
            'status': 'todo',
            'due_date': today + timedelta(days=14),
            'created_by': bob,
            'assigned_to': None,
        },
        {
            'title': 'User feedback survey',
            'description': 'Create and distribute a user feedback survey to gather insights for the next sprint.',
            'priority': 'low',
            'status': 'done',
            'due_date': today - timedelta(days=3),
            'created_by': alice,
            'assigned_to': alice,
        },
        {
            'title': 'Performance optimization',
            'description': 'Profile and optimize slow database queries. Target: reduce average page load time by 40%.',
            'priority': 'medium',
            'status': 'in_progress',
            'due_date': today + timedelta(days=10),
            'created_by': bob,
            'assigned_to': john,
        },
    ]

    for task_data in sample_tasks:
        Task.objects.create(**task_data)

    print(f"     ✓ {len(sample_tasks)} sample tasks created")


if __name__ == '__main__':
    setup()
