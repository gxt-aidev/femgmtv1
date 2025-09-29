from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
)

PRIORITY_CHOICES = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
)

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, related_name='tasks_created', on_delete=models.SET_NULL, null=True)
    # assign either to a specific user or assign to a role (one of CustomUser.role values)
    assigned_to = models.ForeignKey(User, related_name='tasks_assigned', on_delete=models.SET_NULL, null=True, blank=True)
    assigned_role = models.CharField(max_length=50, blank=True, null=True,
                                     help_text="If set, the task is for every user with this role.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def is_assigned_to_user(self, user):
        """True if task is assigned directly to `user` or assigned to user's role."""
        if self.assigned_to and self.assigned_to == user:
            return True
        if self.assigned_role and getattr(user, "role", None) == self.assigned_role:
            return True
        return False

    def __str__(self):
        return f"{self.title} [{self.status}]"
