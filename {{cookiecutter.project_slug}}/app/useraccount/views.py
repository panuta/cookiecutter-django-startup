from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _

from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.views import ConfirmEmailView

from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.views import SignupView

from allauth.account.forms import ChangePasswordForm
from allauth.account.utils import logout_on_password_change

from .forms import UserUploadProfileForm, SocialUserSignupForm, UpdateProfileForm, ChangeEmailForm
from .models import User
from .utils_image import get_temp_profile_image_file_details, save_temp_profile_image_from_file, \
    delete_temp_profile_image


def public_profile(request, user_id, user_slug=''):
    user = get_object_or_404(User, id=user_id)

    if user.slug != user_slug:
        return redirect('useraccount:public_profile_with_slug', user_id, user.slug)

    return render(request, 'users/profile.html', {'thisuser': user})


@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            user.display_name = form.cleaned_data['display_name']
            user.save()

            return redirect('useraccount:update_profile')

    else:
        form = UpdateProfileForm(initial={'display_name': user.display_name})

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def update_account(request):
    user = request.user

    if request.method == 'POST':
        submit_value = request.POST.get('submit')

        if submit_value not in ('email', 'resend', 'cancel', 'password'):
            raise Http404

        if submit_value == 'email':
            email_form = ChangeEmailForm(request.user, request.POST)
            if email_form.is_valid():
                email = email_form.cleaned_data['email']
                EmailAddress.objects.add_email(request, user, email, confirm=True)

                return HttpResponseRedirect(reverse('account_email_verification_sent'))

        else:
            email_form = ChangeEmailForm(request.user)

        if submit_value == 'resend':
            user.new_email.send_confirmation()

        if submit_value == 'cancel':
            user.new_email.delete()

        if submit_value == 'password':
            password_form = ChangePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()

                # Prevent user logout by Django when password changed
                logout_on_password_change(request, password_form.user)

                messages.success(request, _('Password is changed'))
                return redirect('useraccount:update_account')

        else:
            password_form = ChangePasswordForm(request.user)

    else:
        email_form = ChangeEmailForm(request.user, initial={'email': request.user.email})
        password_form = ChangePasswordForm(request.user)

    return render(request, 'users/change_password.html', {'email_form': email_form, 'password_form': password_form})


@login_required
@require_POST
def ajax_user_upload_profile_image(request):
    user = request.user

    form = UserUploadProfileForm(request.POST, request.FILES)
    if form.is_valid():
        form.save(user)
        return JsonResponse({'status': 'success'})

    else:
        try:
            error_code = form['file'].errors.as_data()[0].message
        except (TypeError, IndexError):
            error_code = 'response-error'

        return HttpResponseForbidden(error_code)


@login_required
@require_POST
def ajax_user_delete_profile_image(request):
    user = request.user

    if user.profile_image:
        user.profile_image.delete()

    return JsonResponse({'status': 'success'})


# Accounts
# ======================================================================================================================

class UserConfirmEmailView(ConfirmEmailView):

    def get_template_names(self):
        return ['account/email_confirm.html']  # Used when link is invalid

    def get(self, *args, **kwargs):

        try:
            self.object = self.get_object()
        except Http404:
            self.object = None
            return self.render_to_response(self.get_context_data())

        # If user has already confirmed
        if self.object.email_address.verified:
            return render(self.request, 'account/email_confirmed.html', {'email': self.object.email_address.email})

        # If user is currently authenticated but open confirmation email of someone else,
        # ask authenticated user to logout first
        if self.request.user.is_authenticated() and self.request.user != self.object.email_address.user:
            activate_url = reverse('account_confirm_email', args=[self.object.key])
            return redirect('%s?next=%s' % (reverse('account_logout'), activate_url))

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

        if existing_emails:  # Assume that if there's existing email, it means user just change email (not signup).

            # Delete old emails
            EmailAddress.objects.filter(user=user).exclude(primary=True).delete()

            messages.success(self.request, u'Email is changed')
            return redirect('useraccount:update_account')

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
        context = super(SocialUserSignupView, self).get_context_data(**kwargs)

        file_details = get_temp_profile_image_file_details(self.sociallogin)

        temp_profile_image = {'name': file_details['name'], 'size': file_details['size'], 'url': file_details['url']} \
            if file_details else {}

        context.update({'temp_profile_image': temp_profile_image})
        return context


@require_POST
def ajax_user_upload_temp_profile_image(request):
    data = request.session.get('socialaccount_sociallogin')

    if data:
        form = UserUploadProfileForm(request.POST, request.FILES)
        if form.is_valid():
            sociallogin = SocialLogin.deserialize(data)
            imgfile = form.cleaned_data['file']

            save_temp_profile_image_from_file(sociallogin, imgfile)

            return JsonResponse({'status': 'success'})

    return HttpResponseForbidden('response-error')


@require_POST
def ajax_user_delete_temp_profile_image(request):
    data = request.session.get('socialaccount_sociallogin')

    if data:
        sociallogin = SocialLogin.deserialize(data)
        delete_temp_profile_image(sociallogin)

        return JsonResponse({'status': 'success'})

    return HttpResponseForbidden('response-error')
