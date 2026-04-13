"""
Forms for Task Manager Pro.

Provides forms for user registration and task creation/editing
with custom widgets styled for Bootstrap.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task


class UserRegisterForm(UserCreationForm):
    """
    Extended user registration form with email field
    and Bootstrap-styled widgets.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Choose a username'
            elif field_name == 'password1':
                field.widget.attrs['placeholder'] = 'Create a password'
            elif field_name == 'password2':
                field.widget.attrs['placeholder'] = 'Confirm your password'


class TaskForm(forms.ModelForm):
    """
    Form for creating and editing tasks.
    All fields are styled with Bootstrap classes.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title...',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the task in detail...',
                'rows': 4,
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate assigned_to with regular app users only (not superusers)
        self.fields['assigned_to'].queryset = User.objects.filter(
            is_active=True,
            is_superuser=False,
        )
        self.fields['assigned_to'].required = False
        self.fields['assigned_to'].empty_label = '— Unassigned —'
        self.fields['due_date'].required = False
