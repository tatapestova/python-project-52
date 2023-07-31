from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter
from task_manager.labels.models import Labels
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Tasks


class TaskFilter(FilterSet):
    labels = ModelChoiceFilter(
        queryset=Labels.objects.all(),
        label=_('Label')
    )
    personal_tasks = BooleanFilter(
        label=_('Only personal tasks'),
        widget=forms.CheckboxInput,
        method='get_personal_tasks',
    )

    def get_personal_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'labels']
