from django.urls import reverse_lazy
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Tasks
from task_manager.users.models import User
from task_manager.users.mixins import AuthRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.utils.translation import gettext as _


class TaskCreationView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_message = _('Task succesfully created')
    success_url = reverse_lazy('tasks_list')
    extra_context = {
        'create_task': _('Create task'),
        'create': _('Create'),
    }

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)


class TasksListView(AuthRequiredMixin, ListView):
    template_name = 'tasks/tasks_list.html'
    model = Tasks


class TaskDetailView(AuthRequiredMixin, DetailView):
    template_name = 'tasks/task_detail.html'
    model = Tasks


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = TaskForm
    template_name = 'tasks/update.html'
    model = Tasks
    success_message = _('Task succesfully changed')
    success_url = reverse_lazy('tasks_list')
    extra_context = {'update_task': _('Task change'),
                     'change': _('Change')}


class TaskDeleteView(AuthRequiredMixin,
                     SuccessMessageMixin,
                     UserPassesTestMixin,
                     DeleteView):
    model = Tasks
    success_message = _('Task succesfully deleted')
    success_url = reverse_lazy('tasks_list')
    template_name = 'tasks/delete.html'
    extra_context = {'name': _('task')}

    def test_func(self):
        task = self.get_object()
        return self.request.user.username == task.author.username

    def handle_no_permission(self):
        messages.error(self.request,
                       _('A task can only be deleted by its author'))
        return redirect('tasks_list')
