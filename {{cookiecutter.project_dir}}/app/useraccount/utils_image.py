# -*- coding: utf-8 -*-
import imghdr
import urllib, subprocess, urlparse

from PIL import Image
from StringIO import StringIO

import os
import os.path
import requests
import facebook

from easy_thumbnails.files import ThumbnailFile, get_thumbnailer
from easy_thumbnails.namers import default as default_thumbnail_namer

from django.core.files import File
from django.conf import settings

from {{cookiecutter.project_slug}}.common.utils import split_filepath
from {{cookiecutter.project_slug}}.useraccount.models import get_user_profile_image_relpath, get_temp_user_profile_image_relpath, \
    get_temp_user_profile_image_filename


def check_uploading_image(imgfile, upload_setting):
    upload_setting = settings.UPLOAD_SETTINGS[upload_setting]

    if imgfile.size > upload_setting['max_size_in_bytes']:
        return 'file-too-big'

    if not imghdr.what(imgfile):
        return 'invalid-file-type'

    # TODO : use Pillow Image.verify()

    return ''


def has_default_social_profile_image(sociallogin):
    provider = sociallogin.account.get_provider().id

    if provider == 'facebook':
        oauth_args = dict(client_id=settings.FACEBOOK_APP_ID,
                          client_secret=settings.FACEBOOK_SECRET_KEY,
                          grant_type='client_credentials')
        oauth_curl_cmd = ['curl', 'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]
        oauth_response = subprocess.Popen(oauth_curl_cmd,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE).communicate()[0]

        try:
            oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
        except KeyError:
            return False

        graph_api = facebook.GraphAPI(oauth_access_token)

        data = graph_api.get_connections(
            sociallogin.account.uid, 'picture', fields='is_silhouette', redirect=False)

        is_silhouette = data.get('data').get('is_silhouette')
        return is_silhouette

    elif provider == 'twitter':
        # TODO
        pass

    return False


def save_profile_image_from_url(user, avatar_url):
    try:
        req = requests.get(avatar_url)
    except requests.exceptions.RequestException:
        return False

    img = Image.open(StringIO(req.content))

    img_path = get_user_profile_image_relpath(user, 'avatar.jpg')

    filename = '%s/%s' % (settings.MEDIA_ROOT, img_path)
    root, name, ext = split_filepath(filename)

    if not os.path.exists(root):
        os.makedirs(root)

    from easy_thumbnails.processors import colorspace
    img = colorspace(img)

    img.save('%s/%s' % (settings.MEDIA_ROOT, img_path))
    img.close()

    try:
        user.profile_image = ThumbnailFile(img_path)
        user.save()
    except:
        return False

    return True


def save_temp_profile_image_from_url(sociallogin):

    if has_default_social_profile_image(sociallogin):
        return False

    try:
        req = requests.get(sociallogin.account.get_avatar_url())
    except requests.exceptions.RequestException:
        return False

    img = Image.open(StringIO(req.content))

    img_path = get_temp_user_profile_image_relpath(sociallogin)

    filepath = '%s/%s' % (settings.MEDIA_ROOT, img_path)
    root, name, ext = split_filepath(filepath)

    if not os.path.exists(root):
        os.makedirs(root)

    from easy_thumbnails.processors import colorspace
    img = colorspace(img)

    img.save(filepath)
    img.close()

    # Generate thumbnail for uploader
    img_file = open(filepath)
    thumbnailer = get_thumbnailer(img_file, relative_name=get_temp_user_profile_image_relpath(sociallogin))
    thumbnailer.get_thumbnail(settings.THUMBNAIL_ALIASES['']['user_profile_uploader_thumbnail'])

    return True


def save_temp_profile_image_from_file(sociallogin, imgfile):
    filepath = '%s/%s' % (settings.MEDIA_ROOT, get_temp_user_profile_image_relpath(sociallogin))

    dest = open(filepath, 'wb')
    for chunk in imgfile.chunks():
        dest.write(chunk)

    dest = open(filepath, 'rb')

    thumbnailer = get_thumbnailer(dest, relative_name=get_temp_user_profile_image_relpath(sociallogin))
    thumbnailer.get_thumbnail(settings.THUMBNAIL_ALIASES['']['user_profile_uploader_thumbnail'])

    dest.close()


def delete_temp_profile_image(sociallogin):
    filename = get_temp_user_profile_image_filename(sociallogin)
    filepath = '%s/%s' % (settings.MEDIA_ROOT, get_temp_user_profile_image_relpath(sociallogin))

    try:
        img_file = open(filepath)
        thumbnailer = get_thumbnailer(img_file, relative_name=get_temp_user_profile_image_relpath(sociallogin))

        thumbnail_filename = default_thumbnail_namer(
            thumbnailer,
            thumbnailer.get_options(settings.THUMBNAIL_ALIASES['']['user_profile_uploader_thumbnail']).prepared_options(),
            filename,
            settings.TEMP_PROFILE_IMAGE_FILE_TYPE
        )

        thumbnail_filepath = '%s/%s/%s' % (settings.MEDIA_ROOT, settings.TEMP_PROFILE_IMAGE_DIR, thumbnail_filename)

        img_file.close()

        try:
            os.remove(thumbnail_filepath)
        except OSError:
            pass

        try:
            os.remove(filepath)
        except OSError:
            pass

    except IOError:
        pass


def get_temp_profile_image_file_details(sociallogin):
    filename = get_temp_user_profile_image_filename(sociallogin)
    filepath = '%s/%s' % (settings.MEDIA_ROOT, get_temp_user_profile_image_relpath(sociallogin))

    try:
        img_file = open(filepath)
    except IOError:
        return None

    # TODO : What if there's no thumbnail

    thumbnailer = get_thumbnailer(img_file, relative_name=get_temp_user_profile_image_relpath(sociallogin))

    thumbnail_filename = default_thumbnail_namer(
        thumbnailer,
        thumbnailer.get_options(settings.THUMBNAIL_ALIASES['']['user_profile_uploader_thumbnail']).prepared_options(),
        filename,
        settings.TEMP_PROFILE_IMAGE_FILE_TYPE
    )

    img_file.close()

    return {
        'name': filename,
        'size': os.path.getsize(filepath),
        'url': '%s/%s/%s' % (settings.MEDIA_URL, settings.TEMP_PROFILE_IMAGE_DIR, thumbnail_filename),
    }


def has_temp_profile_image(sociallogin):
    filepath = '%s/%s' % (settings.MEDIA_ROOT, get_temp_user_profile_image_relpath(sociallogin))
    return os.path.isfile(filepath)


def persist_temp_profile_image(sociallogin, user):
    temp_filepath = '%s/%s' % (settings.MEDIA_ROOT, get_temp_user_profile_image_relpath(sociallogin))
    profile_image_path = '%s/%s' % (settings.MEDIA_ROOT, get_user_profile_image_relpath(user, temp_filepath))

    if os.path.exists(temp_filepath):
        profile_image_file = open(temp_filepath)
        profile_image_djangofile = File(profile_image_file)

        user.profile_image.save(profile_image_path, profile_image_djangofile)
        user.save()

        profile_image_file.close()

        delete_temp_profile_image(sociallogin)
