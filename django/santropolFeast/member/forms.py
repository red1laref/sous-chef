from django import forms


class ClientBasicInformation (forms.Form):

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    gender = forms.CheckboxInput()

    birthday = forms.DateField()

    phone_number = forms.CharField()

    alert = forms.CharField()


class ClientAddressInformation(forms.Form):

    street_number = forms.IntegerField()

    apartment_number = forms.IntegerField()

    floor_number = forms.IntegerField()

    street_name = forms.CharField(max_length=100)

    city_name = forms.CharField(max_length=50)

    postal_code = forms.CharField(max_length=6)


class MemberRestrictionsInformation(forms.Form):
    pass

    # Suppose to be many to many
    # client_restriction = forms


class ClientAllergyInformation(forms.Form):
    pass


class ClientReferentInformation(forms.Form):

    referent_first_name = forms.CharField(max_length=100)
    referent_last_name = forms.CharField(max_length=100)

    gender = forms.CheckboxInput()


class ClientPaymentInformation(forms.Form):

    billing_type = forms.ChoiceField()

    billing_first_name = forms.CharField()

    billing_last_name = forms.CharField()

    billing_street_number = forms.IntegerField()

    billing_apartment_number = forms.IntegerField()

    billing_floor_number = forms.IntegerField()

    billing_street_name = forms.CharField()

    billing_city_name = forms.CharField()

    billing_postal_code = forms.CharField()
