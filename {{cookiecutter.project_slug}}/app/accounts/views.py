from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.views import ConfirmEmailView
from allauth.socialaccount.views import SignupView

from app.accounts.forms import SocialUserSignupForm


class UserConfirmEmailView(ConfirmEmailView):

    def get_template_names(self):
        return ['account/email_confirm.html']  # Only used when link is invalid

    def get(self, *args, **kwargs):

        try:
            self.object = self.get_object()
        except Http404:
            self.object = None
            return self.render_to_response(self.get_context_data())

        # If user has already confirmed
        if self.object.email_address.verified:
            return render(self.request, 'account/email_already_confirmed.html', {
                'email': self.object.email_address.email})

        # If user is currently authenticated but open confirmation email of someone else,
        # ask authenticated user to logout first
        if self.request.user.is_authenticated and self.request.user != self.object.email_address.user:
            activate_url = reverse('account_confirm_email', args=[self.object.key])
            return redirect('%s?flag=confirm_on_authenticated&next=%s' % (reverse('account_logout'), activate_url))

        # Confirm email on GET
        self.object.confirm(self.request)
        self.object.email_address.set_as_primary()

        from allauth.account.utils import user_pk_to_url_str

        # Allauth prevent login on email confirmation if confirmation link was opened from another browser session.
        get_adapter(self.request).stash_user(self.request, user_pk_to_url_str(self.object.email_address.user))
        self.login_on_confirm(self.object)

        user = self.object.email_address.user
        email = self.object.email_address.email
        existing_emails = EmailAddress.objects.filter(user=user).exclude(email__iexact=email)

        if existing_emails:  # Assume that if there's existing email, it means user just change email (not signing up).

            # Delete old emails
            EmailAddress.objects.filter(user=user).exclude(primary=True).delete()

            messages.success(self.request, _('Email is changed'))
            return redirect('users:settings_profile')

        return redirect(settings.LOGIN_REDIRECT_URL)

    def post(self, *args, **kwargs):
        # Not in used
        raise Http404


class SocialUserSignupView(SignupView):
    """
    SocialUserSignupView page is for user who signed up with social network, but has no existing email account.
    """
    form_class = SocialUserSignupForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['socialuser'] = self.sociallogin.user
        return context
