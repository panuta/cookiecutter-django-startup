from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django import forms
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import BaseSignupForm, SetPasswordField
from allauth.account.forms import ResetPasswordForm as AllAuthResetPasswordForm
from allauth.account.models import EmailAddress

from allauth.socialaccount.forms import SignupForm

from .utils_image import check_uploading_image
from .utils import social_user_display_name


class UpdateProfileForm(forms.Form):
    display_name = forms.CharField(label=_('Display name'), required=True)


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(required=True)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeEmailForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email == self.user.email:
            raise forms.ValidationError(_('You have not change email'))

        if EmailAddress.objects.filter(email=email).exclude(user=self.user).exists():
            raise forms.ValidationError(_('Another user is already using this email'))

        return email


class UserUploadProfileForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        upload_file = self.cleaned_data['file']
        error_code = check_uploading_image(upload_file, 'user_profile')

        if error_code:
            raise forms.ValidationError(error_code)

        return upload_file

    def save(self, user):
        upload_file = self.cleaned_data['file']

        if user.profile_image:
            user.profile_image.delete()

        user.profile_image = upload_file
        user.save()


# Below is to override allauth forms

class EmailUserSignupForm(BaseSignupForm):
    display_name = forms.CharField(label=_('Display name'), required=True)
    password1 = SetPasswordField(label=_('Password'), )

    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)

        user.display_name = self.cleaned_data['display_name']
        user.save()

        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class SocialUserSignupForm(SignupForm):
    password1 = SetPasswordField(label=_('Password'), required=True)
    display_name = forms.CharField(label=_('Display name'), max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super(SocialUserSignupForm, self).__init__(*args, **kwargs)

        self.fields['email'].initial = self.sociallogin.user.email

        if self.sociallogin.user.email:
            self.fields['email'].widget.attrs['readonly'] = True

        self.fields['display_name'].initial = social_user_display_name(self.sociallogin.user)

    def save(self, request):

        # Check if user submitted different email we got from social network (Nasty user)
        if self.sociallogin.user.email and self.sociallogin.user.email != self.cleaned_data.get('email'):
            self.cleaned_data['email'] = self.sociallogin.user.email

        user = super(SocialUserSignupForm, self).save(request)
        user.display_name = self.cleaned_data['display_name']
        user.save()


class ResetPasswordForm(AllAuthResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']

        # Check if user reset with unverified email
        mails = EmailAddress.objects.filter(email__iexact=email, verified=False)
        if mails.exists():
            raise forms.ValidationError(_('The e-mail address is not assigned to any user account'))

        return super(ResetPasswordForm, self).clean_email()
