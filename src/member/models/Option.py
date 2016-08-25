from django.db import models
from django.utils.translation import ugettext_lazy as _

class Option(models.Model):

    OPTION_GROUP_CHOICES = (
        ('main dish size', _('Main dish size')),
        ('dish', _('Dish')),
        ('preparation', _('Preparation')),
        ('other order item', _('Other order item')),
    )

    class Meta:
        verbose_name_plural = _('options')

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

    option_group = models.CharField(
        max_length=100,
        choices=OPTION_GROUP_CHOICES,
        verbose_name=_('option group')
    )

    def __str__(self):
        return self.name
