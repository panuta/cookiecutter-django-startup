from allauth.account.models import EmailAddress
from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .models import User


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        social_email = sociallogin.email_addresses[0].email if sociallogin.email_addresses else ''

        try:
            email_user = User.objects.get(email=social_email)
        except User.DoesNotExist:
            email_user = None

        # If user signed up using email but not yet verified, and used Social Network account for signup,
        # we deliberately verify it (with assumption that email from social network is already verified).
        try:
            unverified_email = EmailAddress.objects.get(user=email_user, verified=False)
            get_account_adapter(request).confirm_email(request, unverified_email)
        except EmailAddress.DoesNotExist:
            pass

        # If user already have account registered by email, it will connect them together.
        if email_user and not sociallogin.is_existing:
            sociallogin.connect(request, email_user)
