from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Labels
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.mixins import AuthRequiredMixin, DeleteProtectionMixin


class LabelsListView(AuthRequiredMixin, ListView):
    template_name = 'labels/labels_list.html'
    model = Labels


class LabelCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'labels/create.html'
    model = Labels
    form_class = LabelForm
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully created')
    extra_context = {
        'create_label': _('Create label'),
        'create': _('Create'),
    }


class LabelUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'labels/update.html'
    model = Labels
    form_class = LabelForm
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully changed')
    extra_context = {
        'update_label': _('Update label'),
        'change': _('Change'),
    }


class LabelDeleteView(AuthRequiredMixin, DeleteProtectionMixin,
                      SuccessMessageMixin, DeleteView):

    template_name = 'labels/delete.html'
    model = Labels
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully deleted')
    protected_message = _('It is not possible to delete a label '
                          'because it is in use')
    protected_url = reverse_lazy('labels_list')
