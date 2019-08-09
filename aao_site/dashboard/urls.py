from django.urls import path

from .views import DashboardPageView

urlpatterns = [
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
]
