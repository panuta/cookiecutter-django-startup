from django.urls import include, path

from . import views

app_name = 'useraccount'

users_urlpatterns = [
    path(regex='update/profile/', view=views.update_profile, name='update_profile'),
    path(regex='update/account/', view=views.update_account, name='update_account'),

    path('(?P<user_id>\d+)/', views.public_profile, {'user_slug': ''}, name='public_profile'),
    path('(?P<user_id>\d+)/(?P<user_slug>.+)/', views.public_profile, name='public_profile_with_slug'),
]

allauth_urlpatterns = [
    path('confirm-email/(?P<key>\w+)/', views.UserConfirmEmailView.as_view(), name='confirm_email'),
    path('social/signup/', views.SocialUserSignupView.as_view(), name='socialaccount_signup'),
    path('', include('allauth.urls')),
]

urlpatterns = [
    # for uploading user image
    # url(r'^change-email/$', views.change_email, name='change_email'),

    path('users/', include(users_urlpatterns)),
    path('accounts/', include(allauth_urlpatterns)),
]
