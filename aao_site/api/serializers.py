from rest_framework import serializers

from .models import (
    Event,
    ActiveOdd,
    AllOdd,
    Coupon,
    Bet,
)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class AllOddSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllOdd
        fields = '__all__'


class ActiveOddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveOdd
        exclude = ('event',)


class EventOddSerializer(serializers.ModelSerializer):
    odds = ActiveOddSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'odds',)


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        exclude = ('coupon',)


class CouponBetSerializer(serializers.ModelSerializer):
    bets = BetSerializer(many=True)

    class Meta:
        model = Coupon
        exclude = ('user',)


class CouponSerializer(serializers.ModelSerializer):
    bets = BetSerializer(many=True, write_only=True)

    class Meta:
        model = Coupon
        exclude = ('user',)
        read_only_fields = ('status',)

    def run_validation(self, data=serializers.empty):
        # overwrite the check in db method, then continue with other validators
        self.check_bets(data.get('bets', []))
        return super().run_validation(data)

    @staticmethod
    def check_bets(bets):
        error_list = []
        for bet in bets:
            id_, type_, option = bet['odd'], bet['type'], bet['option']
            odd = ActiveOdd.objects.filter(id=id_)
            if not odd:
                msg = f'Invalid odd {id_} - does not exist in active odds'
                error_list.append({"odd": [msg]})
                continue
            if not getattr(odd.first(), type_):
                msg = f'Invalid {type_} - odd value for this type is null'
                error_list.append({"type": [msg]})
                continue
            if not getattr(odd.first(), type_).get(option):
                msg = (f'Invalid option - '
                       f'{option} is not a valid option for {type_}')
                error_list.append({"type": [msg]})
        if error_list:
            raise serializers.ValidationError({"bets": error_list})

    def validate_bets(self, value):
        if not value:
            msg = 'Ensure this list contains at least one element.'
            raise serializers.ValidationError(msg)
        if len(set(bet['odd'].bookmaker for bet in value)) > 1:
            msg = 'Can\'t create coupon with odds from differnt bookmakers'
            raise serializers.ValidationError(msg)
        odds = [bet['odd'] for bet in value]
        if len(set(odds)) < len(odds):
            msg = 'Can\'t create coupon with due to odds repetitions'
            raise serializers.ValidationError(msg)
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        bets = validated_data.pop('bets')
        coupon = Coupon.objects.create(user=user, **validated_data)
        for bet in bets:
            Bet.objects.create(coupon=coupon, **bet)
        return coupon
