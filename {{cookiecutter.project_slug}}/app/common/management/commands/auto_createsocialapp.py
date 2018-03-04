import os

from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Automatically create default SocialApp for each provider'

    def handle(self, *args, **options):
        sites = Site.objects.all()

        available_providers = providers.registry.get_list()
        for provider in available_providers:
            client_id = os.environ.get('SOCIALACCOUNT_{}_CLIENT_ID'.format(provider.id.upper()))
            secret = os.environ.get('SOCIALACCOUNT_{}_SECRET'.format(provider.id.upper()))

            if client_id and secret:
                socialapp, created = SocialApp.objects.get_or_create(provider=provider.id, defaults={
                    'name': 'Default {}'.format(provider.name),
                    'client_id': client_id,
                    'secret': secret,
                })

                if created:
                    socialapp.sites.add(*sites)
