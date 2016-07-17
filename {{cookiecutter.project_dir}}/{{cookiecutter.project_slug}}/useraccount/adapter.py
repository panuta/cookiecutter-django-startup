from {{cookiecutter.project_slug}}.useraccount.models import User

from allauth.account.models import EmailAddress
from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .utils_image import save_temp_profile_image_from_url, has_temp_profile_image, persist_temp_profile_image, \
    save_profile_image_from_url


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

            if not email_user.profile_image:
                save_profile_image_from_url(email_user, sociallogin.account.get_avatar_url())

        # Load user profile image from social network to temp, unless user already have one.
        if not email_user:
            save_temp_profile_image_from_url(sociallogin)

    def save_user(self, request, sociallogin, form=None):
        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form=form)

        if has_temp_profile_image(sociallogin):
            # If within social signup page user uploaded profile image, we will save it to user.profile_image
            persist_temp_profile_image(sociallogin, user)

        return user
