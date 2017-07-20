from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views

from app.views import bad_request, server_error

urlpatterns = [
    url(settings.ADMIN_URL, include(admin.site.urls)),

    url(r'', include('app.pages.urls', namespace='pages')),
    # url(r'', include('app.dashboard.urls', namespace='dashboard')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'app.views.bad_request'
handler500 = 'app.views.server_error'

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', bad_request),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', server_error),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
