from django.conf import settings


def project_settings(request):
    return {
        'UPLOAD_SETTINGS': settings.UPLOAD_SETTINGS,
    }