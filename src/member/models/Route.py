from django.db import models
from django.utils.translation import ugettext_lazy as _

class Route(models.Model):

    class Meta:
        verbose_name_plural = _('Routes')

    # Information about options added to the meal
    name = models.CharField(
        max_length=50,
        verbose_name=_('name')
    )

    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
