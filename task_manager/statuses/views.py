from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Statuses
from task_manager.users.mixins import AuthRequiredMixin, DeleteProtectionMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView



class StatusCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):

    template_name = 'statuses/create.html'
    model = Statuses
    form_class = StatusForm
    success_url = reverse_lazy('status_list')
    success_message = _('Status successfully created')
    extra_context = {
        'create_status': _('Create status'),
        'create': _('Create'),
    }


class StatusesListView(AuthRequiredMixin, SuccessMessageMixin, ListView):
    template_name = 'statuses/statuses_list.html'
    model = Statuses


class StatusUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'statuses/update.html'
    model = Statuses
    form_class = StatusForm
    success_url = reverse_lazy('status_list')
    success_message = _('Status successfully changed')
    extra_context = {
        'update_status': _('Change status'),
        'update': _('Change'),
    }


class StatusDeleteView(AuthRequiredMixin, DeleteProtectionMixin,
                       SuccessMessageMixin, DeleteView):
    template_name = 'statuses/delete.html'
    model = Statuses
    success_url = reverse_lazy('status_list')
    success_message = _('Status successfully deleted')
    protected_message = _('It is not possible to delete a status '
                          'because it is in use')
    protected_url = reverse_lazy('status_list')
