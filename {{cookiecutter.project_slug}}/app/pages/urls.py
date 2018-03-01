from django.urls import path

from . import views

app_name = 'pages'
urlpatterns = [
    path('', view=views.homepage, name='homepage'),

]
