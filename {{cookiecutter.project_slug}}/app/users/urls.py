from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('update/profile/', view=views.update_profile, name='update_profile'),
    path('update/account/', view=views.update_account, name='update_account'),

    path('<int:user_id>/', views.public_profile, {'user_slug': ''}, name='public_profile'),
]
