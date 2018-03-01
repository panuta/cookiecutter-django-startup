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
