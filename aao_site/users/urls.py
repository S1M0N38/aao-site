from django.urls import path

from .views import LoginPage, LogoutPage, SignupPage

urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutPage.as_view(), name='logout'),
    path('signup/', SignupPage.as_view(), name='signup'),
]
