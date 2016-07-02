# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from . import views

urlpatterns = [

    url(r'^confirm-email/(?P<key>\w+)/$', views.UserConfirmEmailView.as_view(), name='confirm_email'),

    url('^social/signup/$', views.SocialUserSignupView.as_view(), name='socialaccount_signup'),

    url(r'^', include('allauth.urls')),
]
