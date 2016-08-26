from django.db import models
from django.utils.translation import ugettext_lazy as _

from .client import Client
from meal.models import Component, Ingredient

class Client_avoid_ingredient(models.Model):

    client = models.ForeignKey(
        Client,
        verbose_name=_('client'),
        related_name='client_avoid_ingredients'
    )

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name=_('ingredient'),
        related_name='+')

    def __str__(self):
        return "{} {} <has> {}".format(self.client.member.firstname,
                                       self.client.member.lastname,
                                       self.ingredient.name)
