# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.utils.translation import gettext as _
from task_manager.users.forms import UserCreation
from task_manager.users.mixins import (
    AuthRequiredMixin,
    UserPermissionMixin,
    DeleteProtectionMixin
)


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/user_list.html'


class CreateUserView(SuccessMessageMixin,
                     CreateView):
    form_class = UserCreation
    template_name = 'users/create.html'
    success_message = _('User succesfully registered')
    success_url = reverse_lazy('login')
    extra_context = {'registration': _('Registration'),
                     'register': _('To create')}


class UpdateUserView(AuthRequiredMixin, 
                     SuccessMessageMixin,
                     UserPermissionMixin,
                     UpdateView):
    login_url = '/login/'
    form_class = UserCreation
    model = get_user_model()
    success_message = _('User succesfully changed')
    permission_message = _('You do not have permission to modify another user')
    success_url = reverse_lazy('user_list')
    permission_url = 'user_list'
    template_name = 'users/update.html'
    extra_context = {'user_modification': _('User modification'),
                     'change': _('Change')}


class DeleteUserView(AuthRequiredMixin,
                     DeleteProtectionMixin,
                     SuccessMessageMixin,
                     UserPermissionMixin,
                     DeleteView):
    login_url = '/login/'
    permission_url = 'user_list'
    model = get_user_model()
    success_message = _('User succesfully deleted')
    permission_message = _('User cannot be deleted because it is in use')
    success_url = reverse_lazy('user_list')
    template_name = 'users/delete.html'
    context_object_name = 'user'
