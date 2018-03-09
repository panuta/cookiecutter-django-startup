
def social_user_display_name(sociallogin_user):
    if sociallogin_user.last_name:
        display_name = '%s %s' % (sociallogin_user.first_name, sociallogin_user.last_name)
    else:
        display_name = '%s' % sociallogin_user.first_name

    return display_name


def findall_urls(text):
    import re
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return urls


def strip_url_to_path(url_in_full):
    import re
    striped_url = re.sub('http[s]?://', '', url_in_full)
    return striped_url[striped_url.find('/'):]
