from django.conf.urls import url

from . import views

urlpatterns = [
    # for uploading user image
    # url(r'^change-email/$', views.change_email, name='change_email'),

    url(regex=r'^update/profile/', view=views.update_profile, name='update_profile'),
    url(regex=r'^update/account/', view=views.update_account, name='update_account'),

    url(r'^(?P<user_id>\d+)/$', views.public_profile, {'user_slug': ''}, name='public_profile'),
    url(r'^(?P<user_id>\d+)/(?P<user_slug>.+)/$', views.public_profile, name='public_profile_with_slug'),

    url(r'^profile/image/upload/$', views.ajax_user_upload_profile_image, name='upload_profile_image'),
    url(r'^profile/image/delete/$', views.ajax_user_delete_profile_image, name='delete_profile_image'),

    url(r'^profile/image/temp/upload/$', views.ajax_user_upload_temp_profile_image, name='upload_temp_profile_image'),
    url(r'^profile/image/temp/delete/$', views.ajax_user_delete_temp_profile_image, name='delete_temp_profile_image'),

]
