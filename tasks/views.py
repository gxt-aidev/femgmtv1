from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .models import Task
from .forms import TaskForm
from django.contrib.auth import get_user_model

User = get_user_model()

def is_manager_or_admin(user):
    return user.is_authenticated and getattr(user, 'role', None) in ['admin','manager','pmo']

@login_required
def task_list(request):
    """
    Show tasks relevant to the user:
    - tasks assigned directly to the user
    - tasks assigned to user's role
    - tasks created by the user
    Managers/admins see all tasks.
    """
    user = request.user
    if getattr(user, 'role', None) in ['admin','manager','pmo']:
        qs = Task.objects.all().order_by('-created_at')
    else:
        qs = Task.objects.filter(
            Q(assigned_to=user) |
            Q(assigned_role=user.role) |
            Q(created_by=user)
        ).order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': qs})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    # permission: only related users or managers can view
    if not (request.user == task.created_by or task.is_assigned_to_user(request.user) or is_manager_or_admin(request.user)):
        messages.error(request, 'You do not have permission to view this task.')
        return redirect('tasks:task_list')
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    user = request.user
    # if non-manager, prefill assigned_to=self and hide assigned_role in form (handled in template)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.created_by = user
            # If normal user didn't specify assignment, default to them
            if not t.assigned_to and not t.assigned_role:
                t.assigned_to = user
            t.save()
            messages.success(request, 'Task created.')
            return redirect('tasks:task_list')
    else:
        form = TaskForm()
        # Restrict assignment choices for non-manager: prefill assigned_to
        if not is_manager_or_admin(user):
            form.fields['assigned_to'].initial = user
            form.fields['assigned_role'].widget = forms.HiddenInput()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    # permission: only creator, assigned_to, or manager/admin can edit
    if not (request.user == task.created_by or request.user == task.assigned_to or is_manager_or_admin(request.user)):
        messages.error(request, 'You do not have permission to edit this task.')
        return redirect('tasks:task_list')
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated.')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if not (request.user == task.created_by or is_manager_or_admin(request.user)):
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('tasks:task_list')
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('tasks:task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if not (task.is_assigned_to_user(request.user) or request.user == task.created_by or is_manager_or_admin(request.user)):
        messages.error(request, 'You do not have permission to update this task.')
        return redirect('tasks:task_list')
    task.status = 'completed' if task.status != 'completed' else 'pending'
    task.save()
    return redirect('tasks:task_list')
