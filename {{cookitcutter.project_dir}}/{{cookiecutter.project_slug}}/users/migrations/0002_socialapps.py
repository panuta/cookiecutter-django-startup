# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


def update_site_forward(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    site = Site.objects.get(id=settings.SITE_ID)

    SocialApp = apps.get_model('socialaccount', 'SocialApp')
    app, created = SocialApp.objects.get_or_create(provider='facebook', name='facebook', defaults={
        'client_id': settings.FACEBOOK_APP_ID, 'secret': settings.FACEBOOK_SECRET_KEY
    })

    app.sites.add(site)


def update_site_backward(apps, schema_editor):
    SocialApp = apps.get_model('socialaccount', 'SocialApp')
    app = SocialApp.objects.get(provider='facebook', name='facebook')
    app.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('sites', '0002_set_site_domain_and_name'),
    ]

    operations = [
        migrations.RunPython(update_site_forward, update_site_backward),
    ]
