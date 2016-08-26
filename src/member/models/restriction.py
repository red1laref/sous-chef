from django.db import models
from django.utils.translation import ugettext_lazy as _

from .client import Client
from meal.models import Restricted_item

class Restriction(models.Model):

    client = models.ForeignKey(
        Client,
        verbose_name=_('client'),
        related_name='+')

    restricted_item = models.ForeignKey(
        Restricted_item,
        verbose_name=_('restricted item'),
        related_name='+')

    def __str__(self):
        return "{} {} <restricts> {}".format(self.client.member.firstname,
                                             self.client.member.lastname,
                                             self.restricted_item.name)
