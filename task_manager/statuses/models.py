from django.db import models
from django.utils.translation import gettext_lazy as _


class Statuses(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'), unique=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Creation date'))

    def __str__(self):
        return self.name
