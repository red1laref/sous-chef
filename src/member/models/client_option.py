from django.db import models
from django.utils.translation import ugettext_lazy as _

from .client import Client
from .option import Option

class Client_option(models.Model):

    client = models.ForeignKey(
        Client,
        verbose_name=_('client'),
        related_name='+')

    option = models.ForeignKey(
        Option,
        verbose_name=_('option'),
        related_name='+')

    value = models.CharField(
        max_length=100,
        null=True,
        verbose_name=_('value')
    )
    #  value contents depends on option_group of option occurence pointed to:
    #    if option_group = main_dish_size : 'Regular' or 'Large'
    #    if option_group = dish : qty Monday to Sunday ex. '1110120'
    #    if option_group = preparation : Null
    #    if option_group = other_order_item : No occurrence of Client_option

    def __str__(self):
        return "{} {} <has> {}".format(self.client.member.firstname,
                                       self.client.member.lastname,
                                       self.option.name)
