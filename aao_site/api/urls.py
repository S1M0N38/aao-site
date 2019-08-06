from django.urls import path
from rest_framework.authtoken import views

from .views import (
    EventList,
    EventRetrive,
    OddList,
    OddRetrive,
    CouponListCreate,
    CouponRetriveDestroy,
)


urlpatterns = [
    # login
    path('login/', views.obtain_auth_token),
    # events
    path('events/<int:pk>', EventRetrive.as_view()),
    path('events/<str:country>/<str:league>/', EventList.as_view()),
    # odds
    path('odds/<int:pk>', OddRetrive.as_view()),
    path('odds/<str:country>/<str:league>/', OddList.as_view()),
    # coupons
    path('coupons/', CouponListCreate.as_view()),
    path('coupons/<int:pk>', CouponRetriveDestroy.as_view()),
]
