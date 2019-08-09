from django.urls import path

from .views import LoginPage, SignupPage

urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('signup/', SignupPage.as_view(), name='signup'),
]
