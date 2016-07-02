# -*- coding: utf-8 -*-

import os
import re
import string
from django.utils.html import strip_tags


def split_filepath(path):
    (head, tail) = os.path.split(path)
    (root, ext) = os.path.splitext(tail)

    if ext and ext[0] == '.':
        ext = ext[1:]

    return head, root, ext


def email_name(email_address):
    name, separator, domain = email_address.rpartition('@')
    return name


def my_slug(name):
    slug = name.strip()
    slug = strip_tags(slug)
    slug = re.sub('[%s]' % re.escape(string.punctuation), '', slug)
    myre = re.compile(u'('
                      u'\ud83c[\udf00-\udfff]|'
                      u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                      u'[\u2600-\u26FF\u2700-\u27BF])+',
                      re.UNICODE)

    slug = myre.sub('', slug)
    slug = re.sub('[-\s]+', '-', slug)
    slug = slug.lower()
    slug = unicode(slug)
    return slug