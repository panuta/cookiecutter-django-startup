
def social_user_display_name(sociallogin_user):
    if sociallogin_user.last_name:
        display_name = '%s %s' % (sociallogin_user.first_name, sociallogin_user.last_name)
    else:
        display_name = '%s' % sociallogin_user.first_name

    return display_name
