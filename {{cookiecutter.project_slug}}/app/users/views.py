from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import ChangePasswordForm
from allauth.account.models import EmailAddress
from allauth.account.utils import logout_on_password_change

from app.accounts.forms import UpdateProfileForm
from app.accounts.models import User


def public_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/profile.html', {'thisuser': user})


@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            user.display_name = form.cleaned_data['display_name']
            user.save()

            messages.success(request, _('Profile is updated'))
            return redirect('users:update_profile')

    else:
        form = UpdateProfileForm(initial={'display_name': user.display_name})

    return render(request, 'users/profile_update.html', {'form': form})


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

    return render(request, 'templates/users/account_update.html', {'email_form': email_form, 'password_form': password_form})

