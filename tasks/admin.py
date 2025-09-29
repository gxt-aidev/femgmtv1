from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','status','priority','assigned_to','assigned_role','due_date','created_by','created_at')
    list_filter = ('status','priority','assigned_role','created_at')
    search_fields = ('title','description','assigned_to__username','assigned_role','created_by__username')
