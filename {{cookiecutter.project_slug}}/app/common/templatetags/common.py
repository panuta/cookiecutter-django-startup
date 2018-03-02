from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def alert_messages(messages):
    message_html_list = []
    for message in messages:
        if message.tags == 'success':
            tags = 'success'
            icon = 'fas fa-check'
        elif message.tags == 'warning':
            tags = 'warning'
            icon = 'fas fa-exclamation-triangle'
        elif message.tags == 'error':
            tags = 'danger'
            icon = 'fas fa-exclamation-triangle'
        elif message.tags == 'info':
            tags = 'info'
            icon = 'fas fa-info-circle'
        elif message.tags == 'debug':
            tags = 'dark'
            icon = 'fas fa-info-circle'
        else:
            tags = message.tags
            icon = None

        message_html_list.append(
            '<div class="alert{tags}" role="alert">{icon}{message}</div>'.format(
                tags=' alert-{}'.format(tags) if tags else '',
                icon='<i class="{}"></i> '.format(icon) if icon else '',
                message=message))

    return mark_safe(''.join(message_html_list))
