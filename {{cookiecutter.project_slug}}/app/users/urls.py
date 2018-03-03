from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('update/profile/', view=views.settings_profile, name='settings_profile'),
    path('update/social/', view=views.settings_social, name='settings_social'),
    path('update/password/', view=views.settings_password, name='settings_password'),

    path('<int:user_id>/', views.public_profile, name='profile'),
]
