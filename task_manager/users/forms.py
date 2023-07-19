from django.contrib.auth.forms import UserCreationForm
from task_manager.users.models import User


class UserCreation(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
