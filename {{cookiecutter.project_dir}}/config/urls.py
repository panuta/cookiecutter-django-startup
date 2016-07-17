# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views

from {{cookiecutter.project_slug}}.views import bad_request, server_error

urlpatterns = [
    # Django Admin
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # Users
    url(r'^users/', include('{{cookiecutter.project_slug}}.useraccount.urls', namespace='useraccount')),
    url(r'^accounts/', include('{{cookiecutter.project_slug}}.useraccount.urls_allauth')),

    # Pages
    url(r'', include('{{cookiecutter.project_slug}}.pages.urls', namespace='pages')),

    # Your stuff: custom urls includes go here



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = '{{cookiecutter.project_slug}}.views.bad_request'
handler500 = '{{cookiecutter.project_slug}}.views.server_error'

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', bad_request),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', server_error),
    ]
