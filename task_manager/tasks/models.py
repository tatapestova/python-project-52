from django.db import models
from task_manager.statuses.models import Statuses
from django.utils.translation import gettext as _
from task_manager.users.models import User


class Tasks(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Name'))
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name='author',
                               verbose_name=_('Author'))
    description = models.TextField(max_length=10000,
                                   blank=True,
                                   null=True,
                                   verbose_name=_('Description'))
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT,
                               verbose_name=_('Status'))
    executor = models.ForeignKey(User, on_delete=models.PROTECT,
                                 null=True,
                                 blank=True,
                                 related_name='executor',
                                 verbose_name=_('Executor'))
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
