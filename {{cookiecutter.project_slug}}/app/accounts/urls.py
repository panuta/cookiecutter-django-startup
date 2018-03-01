from django.urls import include, path

from . import views


urlpatterns = [
    path('confirm-email/<str:key>/', views.UserConfirmEmailView.as_view(), name='confirm_email'),
    path('social/signup/', views.SocialUserSignupView.as_view(), name='socialaccount_signup'),
    path('', include('allauth.urls')),
]
