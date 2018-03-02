from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('update/profile/', view=views.edit_profile, name='edit_profile'),
    path('update/password/', view=views.change_password, name='change_password'),

    path('<int:user_id>/', views.public_profile, name='profile'),
]
