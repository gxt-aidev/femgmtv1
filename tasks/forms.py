from django.contrib import admin
from .models import Task

# @admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','status','priority','assigned_to','assigned_role','due_date','created_by','created_at')
    list_filter = ('status','priority','assigned_role','created_at')
    search_fields = ('title','description','assigned_to__username','assigned_role','created_by__username')
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','assigned_to','assigned_role','priority','due_date','status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type':'date'}),
            'description': forms.Textarea(attrs={'rows':4})
        }
