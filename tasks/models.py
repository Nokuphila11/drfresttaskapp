from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Custom User model
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username

# Task model
class Task(models.Model):
    # Priority levels
    PRIORITY_LOW = 'Low'
    PRIORITY_MEDIUM = 'Medium'
    PRIORITY_HIGH = 'High'
    
    PRIORITY_LEVELS = (
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    )

    # Status choices
    STATUS_PENDING = 'Pending'
    STATUS_COMPLETED = 'Completed'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)

    # Link to custom User model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    completed_at = models.DateTimeField(null=True, blank=True)  # Field to store completion timestamp

    def clean(self):
        # Validate that the due date is in the future
        if self.due_date < timezone.now().date():
            raise ValidationError("Due date must be in the future.")
        
        # Ensure that if the task is marked completed, the due date is still valid
        if self.status == self.STATUS_COMPLETED and self.due_date < timezone.now().date():
            raise ValidationError("Cannot complete a task with a past due date.")

    def __str__(self):
        return f"{self.title} ({self.get_priority_display()}) - {self.get_status_display()} - Assigned to: {self.user.username if self.user else 'Unassigned'}"

