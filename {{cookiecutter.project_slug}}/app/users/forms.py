from django import forms
from django.utils.translation import ugettext_lazy as _

from allauth.account.models import EmailAddress


class UpdateProfileForm(forms.Form):
    display_name = forms.CharField(
        label=_('Display name'),
        required=True)
    email = forms.EmailField(
        label=_('Email address'),
        required=True)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if EmailAddress.objects.filter(email=email).exclude(user=self.user).exists():
            raise forms.ValidationError(_('This email was already used by another user'))

        return email
