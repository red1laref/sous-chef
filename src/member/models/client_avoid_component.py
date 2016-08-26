from django.db import models
from django.utils.translation import ugettext_lazy as _

from .client import Client
from meal.models import Component

class Client_avoid_component(models.Model):

    client = models.ForeignKey(
        Client,
        verbose_name=_('client'),
        related_name='+')

    component = models.ForeignKey(
        Component,
        verbose_name=_('component'),
        related_name='+')

    def __str__(self):
        return "{} {} <has> {}".format(self.client.member.firstname,
                                       self.client.member.lastname,
                                       self.component.name)
