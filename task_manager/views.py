from django.shortcuts import render
from django.contrib.auth import views
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


class UserLogin(SuccessMessageMixin, views.LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('main')
    success_message = _('You are logged in')


class UserLogout(SuccessMessageMixin, views.LogoutView):
    next_page = reverse_lazy('main')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
