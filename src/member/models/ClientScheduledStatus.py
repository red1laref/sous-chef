from django.db import models

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_filters import FilterSet, MethodFilter, CharFilter, ChoiceFilter, \
    BooleanFilter

from member.models import Client
from note.models import Note

class ClientScheduledStatus(models.Model):
    """ Scheduled status for a client."""

    START = 'START'
    END = 'END'

    CHANGE_STATUS = (
        (START, _('Start')),
        (END, _('End')),
    )

    TOBEPROCESSED = 'NEW'
    PROCESSED = 'PRO'
    ERROR = 'ERR'

    OPERATION_STATUS = (
        (TOBEPROCESSED, _('To be processed')),
        (PROCESSED, _('Processed')),
        (ERROR, _('Error')),
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='scheduled_statuses'
    )

    linked_scheduled_status = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )

    status_from = models.CharField(
        max_length=1,
        choices=Client.CLIENT_STATUS
    )

    status_to = models.CharField(
        max_length=1,
        choices=Client.CLIENT_STATUS
    )

    reason = models.CharField(
        max_length=200,
        blank=True,
        default=''
    )

    change_date = models.DateField(
        auto_now=False,
        auto_now_add=False,
        default=timezone.now,
    )

    change_state = models.CharField(
        max_length=5,
        choices=CHANGE_STATUS,
        default=START
    )

    operation_status = models.CharField(
        max_length=3,
        choices=OPERATION_STATUS,
        default=TOBEPROCESSED
    )

    class Meta:
        ordering = ['change_date']

    def __str__(self):
        return "Update {} status: from {} to {}, on {}".format(
            self.client.member,
            self.get_status_from_display(),
            self.get_status_to_display(),
            self.change_date
        )

    def process(self):
        """ Process a scheduled change if valid."""
        if self.is_valid():
            # Update the client status
            self.client.status = self.status_to
            self.client.save()
            # Update the instance status
            self.operation_status = self.PROCESSED
            self.save()
            # Add note to client
            self.add_note_to_client()
            return True
        else:
            self.operation_status = self.ERROR
            self.save()
            return False

    def is_valid(self):
        """ Returns True if a scheduled change must be applied."""
        return self.client.status == self.status_from \
            and self.operation_status == self.TOBEPROCESSED

    def add_note_to_client(self, author=None):
        """ Create a note associated to self.client."""
        note = Note(
            note=self,
            author=author,
            client=self.client,
        )
        note.save()

class ClientScheduledStatusFilter(FilterSet):
    """ Define filters for scheduled status."""

    ALL = 'ALL'

    operation_status = ChoiceFilter(
        choices=((ALL, _('All')),) + ClientScheduledStatus.OPERATION_STATUS
    )

    class Meta:
        model = ClientScheduledStatus
        fields = ['operation_status']
