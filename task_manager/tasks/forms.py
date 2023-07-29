from django.forms import ModelForm
from task_manager.tasks.models import Tasks


class TaskForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ['name',
                  'description',
                  'status',
                  'executor',
                  'labels'
                  ]
