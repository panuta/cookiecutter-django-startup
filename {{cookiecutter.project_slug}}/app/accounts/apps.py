from django.apps import AppConfig
from django.db.models.signals import post_migrate

from app.accounts.signals import set_social_app


class AccountsConfig(AppConfig):
    name = 'app.accounts'

    def ready(self):
        post_migrate.connect(set_social_app, sender=self)
