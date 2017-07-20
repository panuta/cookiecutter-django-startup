from django.conf import settings


def project_settings(request):
    return {
        'settings': settings,
    }
