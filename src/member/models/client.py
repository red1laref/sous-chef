import math

from django.db import models
from django.db.models import Q

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_filters import FilterSet, MethodFilter, CharFilter, ChoiceFilter, \
    BooleanFilter
from annoying.fields import JSONField

from .member import Member
from .route import Route
# from .restriction import Restriction
from meal.models import COMPONENT_GROUP_CHOICES_MAIN_DISH

class ClientManager(models.Manager):

    def get_birthday_boys_and_girls(self):

        today = datetime.datetime.now()

        return self.filter(
            birthdate__month=today.month,
            birthdate__day=today.day
        )


class ActiveClientManager(ClientManager):

    def get_queryset(self):

        return super(ActiveClientManager, self).get_queryset().filter(
            status=Client.ACTIVE
        )


class PendingClientManager(ClientManager):

    def get_queryset(self):

        return super(PendingClientManager, self).get_queryset().filter(
            status=Client.PENDING
        )


class ContactClientManager(ClientManager):

    def get_queryset(self):

        return super(ContactClientManager, self).get_queryset().filter(
            Q(status=Client.ACTIVE) |
            Q(status=Client.STOPCONTACT) |
            Q(status=Client.PAUSED) |
            Q(status=Client.PENDING)
        )


class Client(models.Model):

    class Meta:
        verbose_name_plural = _('clients')

    DAYS_OF_WEEK = (
        ('monday', _('Monday')),
        ('tuesday', _('Tuesday')),
        ('wednesday', _('Wednesday')),
        ('thursday', _('Thursday')),
        ('friday', _('Friday')),
        ('saturday', _('Saturday')),
        ('sunday', _('Sunday')),
    )

    PAYMENT_TYPE = (
        ('check', _('Check')),
        ('cash', _('Cash')),
        ('debit', _('Debit card')),
        ('credit', _('Credit card')),
        ('eft', _('EFT')),
    )

    RATE_TYPE = (
        ('default', _('Default')),
        ('low income', _('Low income')),
        ('solidary', _('Solidary')),
    )

    RATE_TYPE_LOW_INCOME = RATE_TYPE[1][0]
    RATE_TYPE_SOLIDARY = RATE_TYPE[2][0]

    DELIVERY_TYPE = (
        ('O', _('Ongoing')),
        ('E', _('Episodic')),
    )

    GENDER_CHOICES = (
        ('', _('Gender')),
        ('F', _('Female')),
        ('M', _('Male')),
    )

    # Characters are used to keep a backward-compatibility
    # with the previous system.
    PENDING = 'D'
    ACTIVE = 'A'
    PAUSED = 'S'
    STOPNOCONTACT = 'N'
    STOPCONTACT = 'C'
    DECEASED = 'I'

    CLIENT_STATUS = (
        (PENDING, _('Pending')),
        (ACTIVE, _('Active')),
        (PAUSED, _('Paused')),
        (STOPNOCONTACT, _('Stop: no contact')),
        (STOPCONTACT, _('Stop: contact')),
        (DECEASED, _('Deceased')),
    )

    LANGUAGES = (
        ('en', _('English')),
        ('fr', _('French')),
    )

    billing_member = models.ForeignKey(
        Member,
        related_name='+',
        verbose_name=_('billing member'),
    )

    billing_payment_type = models.CharField(
        verbose_name=_('Payment Type'),
        max_length=10,
        null=True,
        choices=PAYMENT_TYPE,
    )

    rate_type = models.CharField(
        verbose_name=_('rate type'),
        max_length=10,
        choices=RATE_TYPE,
        default='default'
    )

    member = models.ForeignKey(
        Member,
        verbose_name=_('member')
    )

    emergency_contact = models.ForeignKey(
        Member,
        verbose_name=_('emergency contact'),
        related_name='emergency_contact',
        null=True,
    )

    emergency_contact_relationship = models.CharField(
        max_length=100,
        verbose_name=_('emergency contact relationship'),
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=1,
        choices=CLIENT_STATUS,
        default=PENDING
    )

    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        default='fr'
    )

    alert = models.TextField(
        verbose_name=_('alert client'),
        blank=True,
        null=True,
    )

    delivery_type = models.CharField(
        max_length=1,
        choices=DELIVERY_TYPE,
        default='O'
    )

    gender = models.CharField(
        max_length=1,
        default='U',
        blank=True,
        null="True",
        choices=GENDER_CHOICES,
    )

    birthdate = models.DateField(
        auto_now=False,
        auto_now_add=False,
        default=timezone.now,
        blank=True,
        null=True
    )

    route = models.ForeignKey(
        Route,
        verbose_name=_('route'),
        blank=True,
        null=True
    )

    meal_default_week = JSONField(
        blank=True, null=True
    )

    delivery_note = models.TextField(
        verbose_name=_('Delivery Note'),
        blank=True,
        null=True
    )

    def __str__(self):
        return "{} {}".format(self.member.firstname, self.member.lastname)

    objects = ClientManager()

    active = ActiveClientManager()
    pending = PendingClientManager()
    contact = ContactClientManager()

    @property
    def age(self):
        """
        Returns integer specifying person's age in years on the current date.

        >>> from datetime import date
        >>> p = Client(birthdate=date(1950, 4, 19)
        >>> p.age()
        66
        """
        from datetime import date
        current = date.today()

        if current < self.birthdate:
            return 0
        return math.floor((current - self.birthdate).days / 365)

    @property
    def orders(self):
        """
        Returns orders associated to this client
        """
        return self.client_order.all()

    @property
    def restrictions(self):
        """
        Returns restrictions associated to this client
        """
        return Restriction.objects.filter(client=self.id)

    @property
    def food_preparation(self):
        """
        Returns specific food preparation associated to this client
        """
        return Client_option.objects.filter(
            client=self.id,
            option__option_group='preparation'
        )

    @property
    def ingredients_to_avoid(self):
        """
        Returns ingredients to avoid associated to this client
        """
        return Client_avoid_ingredient.objects.filter(
            client=self.id,
        )

    @property
    def components_to_avoid(self):
        """
        Returns component(s) to avoid associated to this client
        """
        return Client_avoid_component.objects.filter(
            client=self.id,
        )

    @property
    def notes(self):
        """
        Returns notes associated to this client
        """
        return self.client_notes.all()

    @property
    def meals_schedule(self):
        """
        Returns a hierarchical dict representing the meals schedule.
        """

        prefs = {}
        for day, str in DAYS_OF_WEEK:
            current = {}
            for component in [
                    'main_dish',
                    'compote',
                    'dessert',
                    'fruit_salad',
                    'green_salad',
                    'pudding']:

                item = self.meal_default_week.get(
                    component + '_' + day + '_quantity'
                ) or 0
                current[component] = item

            size = self.meal_default_week.get(
                'size_' + day
            ) or ''
            current['size'] = size

            if current['main_dish'] == 0:
                prefs[day] = None
            else:
                prefs[day] = current

        return prefs

    @staticmethod
    def get_meal_defaults(client, component_group, day):
        """Get the meal defaults quantity and size for a day.

        # TODO fix keys in wizard code to use Component_group constants

        Static method called only on class object.

        Parameters:
          client : client object
          component_group : as in meal.models.COMPONENT_GROUP_CHOICES
          day : day of week where 0 is monday, 6 is sunday

        Returns:
          (quantity, size)

        Prerequisite:
          client.meal_default_week is a dictionary like
            {
              "compote_friday_quantity": null,
              ...
              "compote_wednesday_quantity": null,
              "dessert_friday_quantity": 2,
              ...
              "dessert_wednesday_quantity": null,
              "diabetic_friday_quantity": null,
              ...
              "fruit_salad_friday_quantity": null,
              "green_salad_friday_quantity": 2,
              "main_dish_friday_quantity": 2,
              "main_dish_wednesday_quantity": 1,
              "pudding_friday_quantity": null,
              "pudding_wednesday_quantity": null,
              "size_friday": "R",
              ...
              "size_saturday": "",
            }
        """

        meals_default = client.meal_default_week
        if meals_default:
            quantity = meals_default.get(
                component_group + '_' + DAYS_OF_WEEK[day][0] + '_quantity'
            ) or 0
            size = meals_default.get('size_' + DAYS_OF_WEEK[day][0]) or ''
        else:
            quantity = 0
            size = ''
        # DEBUG
        # print("client, compgroup, day, qty",
        #       client, component_group, days[day], quantity)
        return quantity, size

    def set_meal_defaults(self, component_group, day, quantity=0, size=''):
        """Set the meal defaults quantity and size for a day.

        Static method called only on class object.

        Parameters:
          component_group : as in meal.models.COMPONENT_GROUP_CHOICES
          day : day of week where 0 is monday, 6 is sunday
          quantity : number of servings of this component_group
          size : size of the serving of this component_group
        """

        if not self.meal_default_week:
            self.meal_default_week = {}
        self.meal_default_week[
            component_group + '_' + DAYS_OF_WEEK[day][0] + '_quantity'
        ] = quantity
        if component_group == COMPONENT_GROUP_CHOICES_MAIN_DISH:
            self.meal_default_week['size_' + DAYS_OF_WEEK[day][0]] = size
        # DEBUG
        # print("SET client, compgroup, day, qty, size, dict",
        #       self, component_group, days[day], quantity, size,
        #       self.meal_default_week)


class ClientFilter(FilterSet):
    pass

    # name = MethodFilter(
    #     action='filter_search',
    #     label=_('Search by name')
    # )
    #
    # status = ChoiceFilter(
    #     choices=(('', ''),) + Client.CLIENT_STATUS,
    # )
    #
    # delivery_type = ChoiceFilter(
    #     choices=(('', ''),) + Client.DELIVERY_TYPE
    # )
    #
    # class Meta:
    #     model = Client
    #     fields = ['route', 'status', 'delivery_type']
    #
    # @staticmethod
    # def filter_search(queryset, value):
    #     if not value:
    #         return queryset
    #
    #     name_contains = Q()
    #     names = value.split(' ')
    #
    #     for name in names:
    #
    #         firstname_contains = Q(
    #             member__firstname__icontains=name
    #         )
    #
    #         lastname_contains = Q(
    #             member__lastname__icontains=name
    #         )
    #
    #         name_contains |= firstname_contains | lastname_contains
    #
    #     return queryset.filter(name_contains)
