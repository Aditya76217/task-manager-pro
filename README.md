# 🚀 TaskManager Pro

A modern, full-stack **task management application** built with Django, Bootstrap 5, and vanilla JavaScript.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)

---

## ✨ Features

### 🔐 Authentication
- User registration with email
- Secure login/logout via Django auth
- Session-based security

### 📋 Kanban Board
- **Three columns**: To Do, In Progress, Done
- **Drag-and-drop** task cards between columns
- Real-time AJAX status updates (no page reload)
- Animated transitions and drop effects

### 📝 Task Management
- Create, edit, view, and delete tasks
- Priority levels: **Low** (green), **Medium** (yellow), **High** (red)
- Due date tracking with overdue indicators
- Task description with rich detail view

### 👥 Team Collaboration
- Assign tasks to team members
- Multiple users can view shared tasks
- User avatar initials on task cards
- Filter tasks by assigned user

### 📊 Progress Tracking
- Overall completion progress bar
- Column task counts
- Done/Total task statistics

### 🔍 Search & Filter
- Search tasks by title or description
- Filter by priority level
- Filter by assigned user
- Clear filters with one click

### 🎨 Design
- Dark theme with glassmorphism effects
- Smooth micro-animations
- Responsive layout (mobile-friendly)
- Color-coded priority badges

---

## 📁 Project Structure

```
TaskManagerPro/
├── manage.py                   # Django management script
├── setup.py                    # Quick setup & seed data
├── requirements.txt            # Python dependencies
├── db.sqlite3                  # SQLite database (auto-generated)
│
├── taskmanager/                # Django project settings
│   ├── __init__.py
│   ├── settings.py             # App configuration
│   ├── urls.py                 # Root URL routing
│   ├── wsgi.py                 # WSGI entry point
│   └── asgi.py                 # ASGI entry point
│
├── tasks/                      # Main application
│   ├── __init__.py
│   ├── admin.py                # Admin panel config
│   ├── apps.py                 # App config
│   ├── forms.py                # User & Task forms
│   ├── models.py               # Task model
│   ├── urls.py                 # App URL patterns
│   ├── views.py                # Views & API endpoints
│   ├── migrations/             # Database migrations
│   └── templatetags/
│       └── task_filters.py     # Custom template filters
│
├── templates/                  # HTML templates
│   ├── base.html               # Base layout
│   ├── registration/
│   │   ├── login.html          # Login page
│   │   └── register.html       # Registration page
│   └── tasks/
│       ├── dashboard.html      # Kanban board
│       ├── task_form.html      # Create/Edit form
│       ├── task_detail.html    # Task detail view
│       └── task_confirm_delete.html
│
└── static/                     # Static assets
    ├── css/
    │   └── style.css           # Custom styles
    └── js/
        └── kanban.js           # Drag-and-drop logic
```

---

## ▶️ Getting Started

### Prerequisites
- **Python 3.10+** installed
- **pip** package manager

### Step-by-Step Setup

```bash
# 1. Navigate to the project directory
cd TaskManagerPro

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install Django
pip install -r requirements.txt

# 4. Run the quick setup (migrations + superuser + sample data)
python setup.py

# 5. Start the development server
python manage.py runserver
```

### 🌐 Access the Application

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000 | Dashboard (requires login) |
| http://127.0.0.1:8000/login | Login page |
| http://127.0.0.1:8000/register | Registration page |
| http://127.0.0.1:8000/admin | Django admin panel |

### 🔑 Default Accounts

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Superuser |
| `alice` | `password123` | Team member |
| `bob` | `password123` | Team member |

---

## 🛠️ Manual Setup (Alternative)

If you prefer not to use `setup.py`:

```bash
# Make migrations
python manage.py makemigrations tasks

# Apply migrations
python manage.py migrate

# Create a superuser manually
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## 🎯 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| `POST` | `/api/task/update-status/` | Update task status (AJAX) |
| `GET` | `/api/task/stats/` | Get task statistics |

### Update Status Request
```json
{
    "task_id": 1,
    "new_status": "in_progress"
}
```

### Update Status Response
```json
{
    "success": true,
    "task_id": 1,
    "new_status": "In Progress",
    "progress_percent": 25,
    "done_count": 1,
    "total_tasks": 4
}
```

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 4.2 (Python) |
| **Frontend** | HTML5, CSS3, JavaScript |
| **UI Framework** | Bootstrap 5.3 |
| **Icons** | Bootstrap Icons |
| **Font** | Google Fonts (Inter) |
| **Database** | SQLite |
| **AJAX** | Fetch API |

---

## 📜 License

This project is open-source and available under the MIT License.
