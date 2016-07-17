# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models

from easy_thumbnails.fields import ThumbnailerImageField
from autoslug.utils import slugify

from {{cookiecutter.project_slug}}.common.utils import split_filepath


def get_user_profile_image_relpath(instance, filename):
    (head, name, ext) = split_filepath(filename)
    return 'users/%s/avatar.%s' % (instance.id, ext)


def get_temp_user_profile_image_filename(sociallogin):
    if sociallogin.user.email:
        filename = sociallogin.user.email
    else:
        filename = sociallogin.account.uid

    return '%s.%s' % (filename, settings.TEMP_PROFILE_IMAGE_FILE_TYPE)


def get_temp_user_profile_image_relpath(sociallogin):
    filename = get_temp_user_profile_image_filename(sociallogin)

    return '%s/%s' % (settings.TEMP_PROFILE_IMAGE_DIR, filename)


def user_display_name(user):
    return user.display_name


class User(AbstractUser):
    profile_image = ThumbnailerImageField(null=True, blank=True,
                                          upload_to=get_user_profile_image_relpath,
                                          resize_source=settings.THUMBNAIL_SAVE_ORIGINAL['user_profile'])

    display_name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.display_name

    def get_absolute_url(self):
        return reverse("account:profile")

    @property
    def slug(self):
        return slugify(self.display_name)

    @property
    def change_email_request(self):
        return self.emailaddress_set.filter(verified=False).last()
