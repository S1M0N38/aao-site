from django.contrib import admin

from .models import Event, ActiveOdd, AllOdd, Coupon, Bet


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'datetime', 'country', 'league',
        'home_team', 'away_team', 'home_goals', 'away_goals',)


@admin.register(ActiveOdd, AllOdd)
class OddAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime', 'bookmaker', 'event',)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'money', 'datetime', 'status',)


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    readonly_fields = ('value',)
    list_display = ('id', 'odd', 'type', 'option', 'coupon', 'value', 'status',)
