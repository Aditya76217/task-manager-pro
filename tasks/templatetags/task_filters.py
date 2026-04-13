"""
Custom template filters for the tasks app.
"""
from django import template

register = template.Library()


@register.filter
def get_initials(user):
    """Get user initials for avatar display."""
    if user and user.first_name and user.last_name:
        return f"{user.first_name[0]}{user.last_name[0]}".upper()
    elif user and user.username:
        return user.username[:2].upper()
    return "?"


@register.filter
def priority_badge_class(priority):
    """Return Bootstrap badge class for priority."""
    classes = {
        'low': 'bg-success',
        'medium': 'bg-warning text-dark',
        'high': 'bg-danger',
    }
    return classes.get(priority, 'bg-secondary')
