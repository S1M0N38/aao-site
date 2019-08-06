from rest_framework import generics

from .models import Event, AllOdd, Coupon
from .serializers import (
    EventSerializer,
    EventOddSerializer,
    AllOddSerializer,
    CouponSerializer,
    CouponBetSerializer,
)


class EventList(generics.ListAPIView):
    """
    API endpoint that allows events to be viewed.
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        country = self.kwargs['country']
        league = self.kwargs['league']
        return Event.objects.filter(country=country, league=league)


class EventRetrive(generics.RetrieveAPIView):
    """
    API endpoint that allows a single event to be viewed (by pk).
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class OddList(generics.ListAPIView):
    """
    API endpoint that allows odds to be viewed.
    """
    serializer_class = EventOddSerializer

    def get_queryset(self):
        country = self.kwargs['country']
        league = self.kwargs['league']
        return Event.objects.filter(country=country, league=league)


class OddRetrive(generics.RetrieveAPIView):
    """
    API endpoint that allows a single odd to be viewed (by pk).
    """
    serializer_class = AllOddSerializer
    queryset = AllOdd.objects.all()


class CouponListCreate(generics.ListCreateAPIView):
    """
    API endpoint that allows coupons to be created or viewed.
    """
    serializer_class = CouponSerializer

    def get_queryset(self):
        return Coupon.objects.filter(user=self.request.user)


class CouponRetriveDestroy(generics.RetrieveDestroyAPIView):
    """
    API endpoint that allows a single coupon to be deleted (by pk).
    """
    serializer_class = CouponBetSerializer

    def get_queryset(self):
        return Coupon.objects.filter(user=self.request.user)
