from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):

    class Meta:
        verbose_name_plural = _('contacts')

    HOME = 'Home phone'
    CELL = 'Cell phone'
    WORK = 'Work phone'
    EMAIL = 'Email'

    CONTACT_TYPE_CHOICES = (
        (HOME, HOME),
        (CELL, CELL),
        (WORK, WORK),
        (EMAIL, EMAIL),
    )

    # Member contact information
    type = models.CharField(
        max_length=100,
        choices=CONTACT_TYPE_CHOICES,
        verbose_name=_('contact type')
    )

    value = models.CharField(
        max_length=50,
        verbose_name=_('value')
    )

    member = models.ForeignKey(
        'member.Member',
        verbose_name=_('member'),
        related_name='member_contact',
    )

    def __str__(self):
        return "{} {}".format(self.member.firstname, self.member.lastname)
