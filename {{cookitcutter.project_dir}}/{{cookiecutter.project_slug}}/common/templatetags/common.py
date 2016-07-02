from django import template
from django.conf import settings

from easy_thumbnails.files import get_thumbnailer

register = template.Library()


@register.filter
def thumbnail(obj, alias):
    if obj:
        return get_thumbnailer(obj)[alias].url
    else:
        field_name = obj.field.__str__()
        empty_thumbnail_settings = settings.EMPTY_THUMBNAIL_ALIASES.get(field_name)

        if empty_thumbnail_settings:
            try:
                thumbnail_settings = settings.THUMBNAIL_ALIASES[field_name][alias]

                thumbnail_file = open('%s/%s' % (settings.APPS_DIR.path('static'), empty_thumbnail_settings['filepath']))
                thumbnailer = get_thumbnailer(thumbnail_file, relative_name=empty_thumbnail_settings['filepath'])
                return thumbnailer.get_thumbnail({
                    'crop': thumbnail_settings['crop'],
                    'size': thumbnail_settings['size'],
                }).url

            except:
                # TODO : Add to logs
                pass

        return ''
