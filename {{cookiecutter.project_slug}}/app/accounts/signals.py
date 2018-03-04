from allauth.socialaccount import providers
from django.apps import apps as global_apps
from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def set_social_app(app_config, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
    SocialApp = apps.get_model('socialaccount', 'SocialApp')

    Site = apps.get_model('sites', 'Site')
    sites = Site.objects.using(using).all()

    available_providers = providers.registry.get_list()
    for provider in available_providers:
        client_id = getattr(settings, 'SOCIALACCOUNT_{}_CLIENT_ID'.format(provider.id.upper()))
        secret = getattr(settings, 'SOCIALACCOUNT_{}_SECRET'.format(provider.id.upper()))

        if client_id and secret:
            socialapp, created = SocialApp.objects.using(using).get_or_create(provider=provider.id, defaults={
                'name': 'Default {}'.format(provider.name),
                'client_id': client_id,
                'secret': secret,
            })

            if created:
                socialapp.sites.add(*sites)
