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
    serializer_class = EventSerializer

    def get_queryset(self):
        country = self.kwargs['country']
        league = self.kwargs['league']
        return Event.objects.filter(country=country, league=league)


class EventRetrive(generics.RetrieveAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class OddList(generics.ListAPIView):
    serializer_class = EventOddSerializer

    def get_queryset(self):
        country = self.kwargs['country']
        league = self.kwargs['league']
        return Event.objects.filter(country=country, league=league)


class OddRetrive(generics.RetrieveAPIView):
    serializer_class = AllOddSerializer
    queryset = AllOdd.objects.all()


class CouponListCreate(generics.ListCreateAPIView):
    serializer_class = CouponSerializer

    def get_queryset(self):
        return Coupon.objects.filter(user=self.request.user)


class CouponRetriveDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = CouponBetSerializer

    def get_queryset(self):
        return Coupon.objects.filter(user=self.request.user)
