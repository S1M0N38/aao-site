from django.urls import path, re_path

from .views import LoginPage, LogoutPage, SignupPage, ActivatePage

urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutPage.as_view(), name='logout'),
    path('signup/', SignupPage.as_view(), name='signup'),
    re_path(
        (r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/'
         r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'),
        ActivatePage, name='activate')
]
