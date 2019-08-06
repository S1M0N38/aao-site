from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from .models import (
    Event,
    AllOdd,
    ActiveOdd,
    Coupon,
)
from .serializers import (
    EventSerializer,
    EventOddSerializer,
    AllOddSerializer,
    CouponSerializer,
    CouponBetSerializer,
)

User = get_user_model()


class TestAuthentication(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = 'test'
        cls.password = 'password'
        cls.user = User.objects.create_user(
            cls.username, 'test@email.com', cls.password)
        cls.token = Token.objects.create(user=cls.user)
        cls.client = APIClient()

    def test_login_get_token(self):
        credentials = {'username': self.username, 'password': self.password}
        response = self.client.post('/api/login/', credentials)
        self.assertEqual(self.token.key, response.json()["token"])

    def test_token_auth_missing(self):
        response = self.client.get('/api/events/england/premier_league/')
        self.assertEqual(response.status_code, 401)

    def test_token_auth_wrong(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token abcdef1234')
        response = self.client.get('/api/events/england/premier_league/')
        self.assertEqual(response.status_code, 401)

    def test_token_auth_right(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/events/england/premier_league/')
        self.assertEqual(response.status_code, 200)


class TestEvents(APITestCase):
    fixtures = ['events', 'users']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.first()
        cls.client = APIClient()

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_get_events_country_league(self):
        country, league = 'england', 'premier_league'
        response = self.client.get(f'/api/events/{country}/{league}/')
        self.assertEqual(response.status_code, 200)
        events = Event.objects.filter(country=country, league=league)
        events_serialized = [EventSerializer(event).data for event in events]
        self.assertEqual(events_serialized, response.json())

    def test_get_events_by_id(self):
        event = Event.objects.first()
        response = self.client.get(f'/api/events/{event.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), EventSerializer(event).data)


class TestOdds(APITestCase):
    fixtures = ['events', 'all_odds', 'active_odds', 'users']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.first()
        cls.client = APIClient()

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_get_odds_by_country_league(self):
        country, league = 'england', 'premier_league'
        response = self.client.get(f'/api/odds/{country}/{league}/')
        self.assertEqual(response.status_code, 200)
        events = Event.objects.filter(country=country, league=league)
        events_serialized = [EventOddSerializer(event).data for event in events]
        self.assertEqual(events_serialized, response.json())

    def test_get_odd_by_id(self):
        odd = AllOdd.objects.first()
        response = self.client.get(f'/api/odds/{odd.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AllOddSerializer(odd).data, response.json())


class TestCoupon(APITestCase):
    fixtures = [
        'events', 'all_odds', 'active_odds', 'bets', 'coupons', 'users']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.first()
        cls.client = APIClient()

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_get_coupons(self):
        response = self.client.get('/api/coupons/')
        self.assertEqual(response.status_code, 200)
        coupons = Coupon.objects.filter(user=self.user).values()
        coupons_serialized = [CouponSerializer(coupon).data for coupon in coupons]
        self.assertEqual(coupons_serialized, response.json())

    def test_get_coupon_by_id(self):
        coupon = Coupon.objects.filter(user=self.user).first()
        response = self.client.get(f'/api/coupons/{coupon.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), CouponBetSerializer(coupon).data)

    def test_delete_coupon_by_id(self):
        coupons = Coupon.objects.filter(user=self.user)
        coupon_deleted = coupons.first()
        response = self.client.delete(f'/api/coupons/{coupon_deleted.id}')
        self.assertEqual(response.status_code, 204)
        self.assertNotIn(coupon_deleted, coupons)

    def test_post_coupon(self):
        bets = []
        old_coupons = Coupon.objects.filter(user=self.user).count()
        odds = ActiveOdd.objects.filter(bookmaker='888sport')[:2]
        for odd in odds:
            bet = {'odd': odd.id, 'type': 'full_time_result', 'option': '1'}
            bets.append(bet)
        coupon = {'money': 10, 'note': 'hello', 'bets': bets}
        response = self.client.post('/api/coupons/', coupon)
        new_coupons = Coupon.objects.filter(user=self.user).count()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(old_coupons + 1, new_coupons)

    def test_post_coupon_null_odd_value(self):
        odd = ActiveOdd.objects.filter(under_over__isnull=True).first()
        bet = {'odd': odd.id, 'type': 'under_over', 'option': 'under'}
        coupon = {'money': 10, 'note': 'hello', 'bets': [bet]}
        response = self.client.post('/api/coupons/', coupon)
        self.assertEqual(response.status_code, 400)

    def test_post_coupon_type_under_over_option_yes(self):
        odd = ActiveOdd.objects.filter(under_over__isnull=False).first()
        bet = {'odd': odd.id, 'type': 'under_over', 'option': 'yes'}
        coupon = {'money': 10, 'note': 'hello', 'bets': [bet]}
        response = self.client.post('/api/coupons/', coupon)
        self.assertEqual(response.status_code, 400)
