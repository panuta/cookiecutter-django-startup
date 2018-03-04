from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Automatically create super user'

    def handle(self, *args, **options):
        user_model = get_user_model()

        if not user_model.objects.filter(is_staff=True).exists():
            try:
                user_model.objects.get(username='admin')
            except user_model.DoesNotExist:
                get_user_model().objects.create_superuser(
                    'admin', '{{cookiecutter.admin_email}}', 'admin')
