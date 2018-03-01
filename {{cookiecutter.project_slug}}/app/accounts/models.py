from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


def user_display_name(user):
    return user.display_name


class User(AbstractUser):
    display_name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.display_name

    def get_absolute_url(self):
        return reverse('useraccount:profile')

    @property
    def change_email_request(self):
        return self.emailaddress_set.filter(verified=False).last()
