from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import ChangePasswordForm
from allauth.account.models import EmailAddress
from allauth.account.utils import logout_on_password_change

from app.accounts.models import User
from app.users.forms import UpdateProfileForm


def public_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/profile.html', {'thisuser': user})


@login_required
def settings_profile(request):
    user = request.user

    if request.method == 'POST':
        submit_value = request.POST.get('submit')

        if submit_value in ('resend', 'cancel'):
            latest_changing_email = request.POST.get('latest_changing_email')

            try:
                latest_changing_email_request = EmailAddress.objects.get(user=user, email=latest_changing_email)
            except EmailAddress.DoesNotExist:
                messages.warning(request, _('There is no request to change to this email'))
                return redirect('users:edit_profile')

            if submit_value == 'resend':
                latest_changing_email_request.send_confirmation()
                messages.success(request, _('Email is sent, please check your inbox'))
                return redirect('users:edit_profile')

            if submit_value == 'cancel':
                latest_changing_email_request.delete()
                messages.success(request, _('Change request is cancelled'))
                return redirect('users:edit_profile')

            return redirect('users:edit_profile')

        else:
            form = UpdateProfileForm(user, request.POST)
            if form.is_valid():
                user.display_name = form.cleaned_data['display_name']
                user.save()

                email = form.cleaned_data['email']
                if user.email != email:
                    EmailAddress.objects.add_email(request, user, email, confirm=True)

                messages.success(request, _('Profile is updated'))
                return redirect('users:edit_profile')

    else:
        form = UpdateProfileForm(user, initial={
            'display_name': user.display_name,
            'email': user.email,
        })

    return render(request, 'users/settings_profile.html', {'form': form})


@login_required
def settings_social(request):
    return render(request, 'users/settings_social.html', {})


@login_required
def settings_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()

            # Prevent user logout by Django when password changed
            logout_on_password_change(request, form.user)

            messages.success(request, _('Password is changed'))
            return redirect('users:change_password')

    else:
        form = ChangePasswordForm(request.user)

    return render(request, 'users/settings_password.html', {'form': form})
