from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from member.views import *
from member.forms import *

urlpatterns = patterns(
    '', url(r'^create/$',
            ClientWizard.as_view(
                    [ClientBasicInformation, ClientAddressInformation,
                     ClientReferentInformation, ClientPaymentInformation]
            )),
    url(_(r'^list/$'),
        ClientList.as_view(), name='list'),
)
