from django.test import LiveServerTestCase
from rest_framework.test import RequestsClient
# As suggest the offcial docs of Django Rest Framework, the best way to test
# the Api for python requests is using RequestsClient.
# 'http://www.django-rest-framework.org/api-guide/testing/#requestsclient'

USERNAME = 'test'
PASSWORD = 'tSPjcAmxeXFY5C4'
TOKEN = 'dd044dddf7b743e63c998aee189db33f2f541ef1'
TOKEN_HEADER = {'Authorization': f'Token {TOKEN}'}
# Sam is pro-gambler and a developer (he knows how to do http requests)
# He want to make more money, but in order to do so he
# have to test his brand new betting strategies.


class MyLiveServerTestCase(LiveServerTestCase):
    fixtures = ['active_odds', 'all_odds', 'bets', 'coupons', 'events',
                'tokens', 'users']

    @classmethod
    def setUpClass(cls):
        cls.c = RequestsClient()
        super().setUpClass()

    def get(self, url, *args, **kwargs):
        url = f'{self.live_server_url}/api/{url}'
        return self.c.get(url, headers=TOKEN_HEADER, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        url = f'{self.live_server_url}/api/{url}'
        return self.c.post(url, headers=TOKEN_HEADER, *args, **kwargs)

    def delete(self, url, *args, **kwargs):
        url = f'{self.live_server_url}/api/{url}'
        return self.c.delete(url, headers=TOKEN_HEADER, *args, **kwargs)


class AuthenticationTest(MyLiveServerTestCase):
    """In order to get the auth-token the user have to post 'username'
    and 'password' to the /login endspoint. After get the token, he have to
    send the token in Headers on every request to aao api.

    POST Endspoint:
    - /api/login
    """

    fixtures = ['tokens', 'users']
    # Sam came across this new site and it's the one he was looking for.

    def test_error_raise_try_request_without_token(self):
        # He try to request for some data but an error message appeare because
        # is not logged in. The error message have a link that redirect to a
        # part of the docs that explain how handle the api authenication.
        url = f'{self.live_server_url}/api/events/england/premier_league/'
        request = self.c.get(url)
        expected_msg = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(request.status_code, 401)
        self.assertDictEqual(request.json(), expected_msg)

    def test_request_with_invalid_token(self):
        # For no reason he try to pass a token that is invalid and that show
        # the error message for invalid token and a link to docs/auth
        url = f'{self.live_server_url}/api/events/england/premier_league/'
        headers = {'Authorization': 'Token 123456789'}
        expected_msg = {'detail': 'Invalid token.'}
        request = self.c.get(url, headers=headers)
        self.assertEqual(request.status_code, 401)
        self.assertDictEqual(request.json(), expected_msg)

    def test_get_token_wrong_user_credentials(self):
        # Now Same knows that to get auth token he needs to send POST request
        # to api/login/ providing 'username' and 'password'.
        # But they are fake
        url = f'{self.live_server_url}/api/login/'
        data = {'username': 'fake_username', 'password': 'fake_password'}
        expected_msg = {'non_field_errors': [
            'Unable to log in with provided credentials.']}
        request = self.c.post(url, data=data)
        self.assertEqual(request.status_code, 400)
        self.assertDictEqual(request.json(), expected_msg)

    def test_request_with_valid_token(self):
        # Ok now he has the credentials of a valid user
        # After reading the docs he had set the auth properly and the api
        # response is 200 code
        url = f'{self.live_server_url}/api/login/'
        data = {'username': USERNAME, 'password': PASSWORD}
        expected_token = TOKEN
        request = self.c.post(url, data=data)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['token'], expected_token)


class EventsTest(MyLiveServerTestCase):
    """The user can only perform GET requests on events

    GET Endspoints:
    - /api/events/<str:country:str>/<str:league>
    - /api/events/<int:pk>
    """
    # Let's look at the events available

    def test_get_events_by_country_league(self):
        # He decided to investigate the english
        # premier league. First request all events in english premier league.
        request = self.get('events/england/premier_league/')
        events = request.json()
        [self.assertEqual('england', e['country']) for e in events]
        [self.assertEqual('premier_league', e['league']) for e in events]

    def test_get_event_by_id(self):
        # A particular event catch his attention so he write down that event
        # id and request only that specific event
        request = self.get('events/england/premier_league/')
        specific_event = request.json()[0]
        request = self.get(f'events/{specific_event["id"]}')
        event = request.json()
        self.assertDictEqual(specific_event, event)


class OddsTest(MyLiveServerTestCase):
    """The user can only perform GET requests on odds

    GET Endspoints:
    - /api/odds/<str:country>/<str:league>
    - /api/odds/<int:pk>
    """
    # And what about the odds?

    def test_get_odds_by_country_league(self):
        # He is now intrested in all odds from premier league so
        # the api return the last odds for every event.
        request = self.get('odds/england/premier_league')
        events = request.json()
        data = [(o['bookmaker'], e['id']) for e in events for o in e['odds']]
        self.assertCountEqual(data, list(set(data)))

    def test_get_odd_by_id(self):
        # Now he want to see a specific odd.
        request = self.get(f'odds/england/premier_league')
        specific_odd = request.json()[0]['odds'][0]
        request = self.get(f'odds/{specific_odd["id"]}')
        odd = request.json()
        self.assertDictContainsSubset(specific_odd, odd)


class CouponTest(MyLiveServerTestCase):
    """The user can perform GET, POST, DELETE requests on coupon

    GET Endspoints:
    - /api/coupons/
    - /api/coupons/<coupons_id:int>

    POST Endspoints:
    - /api/coupons/

    DELETE Endspoints:
    - /api/coupons/<coupons_id:int>
    """
    # It's time to bet! Like on every bookmakers you can place your bet only
    # on last odds
    def get_coupon(self, money=10, note='', bookmaker='888sport', event=0):
        odds = self.get('odds/england/premier_league').json()[event]['odds']
        odd = [o for o in odds if ('bookmaker', bookmaker) in o.items()][0]
        bet = {'odd': odd['id'], 'type': 'full_time_result', 'option': '1'}
        coupon = {'money': money, 'note': note, 'bets': [bet]}
        return coupon

    def test_post_coupon_wrong_keys(self):
        # Sam try to post a new coupon but the format is wrong
        # He need to read the docs better
        coupon = {}
        expected_msg = {'bets': ['This field is required.'],
                        'money': ['This field is required.']}
        request = self.post(f'coupons/', json=coupon)
        self.assertEqual(request.json(), expected_msg)

    def test_post_coupon_money_negative(self):
        expected_msg = {'money': [
            'Ensure this value is greater than or equal to 0.']}
        coupon = self.get_coupon(money=-10)
        request = self.post('coupons/', json=coupon)
        self.assertEqual(request.json(), expected_msg)

    def test_post_coupon_bets_list_empty(self):
        expected_msg = {'bets': [
            'Ensure this list contains at least one element.']}
        coupon = self.get_coupon()
        coupon['bets'] = []
        request = self.post('coupons/', json=coupon)
        self.assertEqual(request.json(), expected_msg)

    def test_post_coupon_odd_id_out_of_index(self):
        # This time the formati is correct but he misspelled the odds_id
        expected_msg = {'bets': [
            {'odd': ['Invalid odd 1 - does not exist in active odds']}]}
        coupon = self.get_coupon()
        coupon['bets'][0]['odd'] = 1
        request = self.post('coupons/', json=coupon)
        self.assertEqual(request.json(), expected_msg)

    def test_post_coupon_single_odd(self):
        # Sam, following the docs guideline, create a coupon that contains only
        # one bet: {bets:[bet], money:100, note:"my first coupon"}
        # Sam is always quite skeptical so he want to check if his new coupon
        # have been already saved with correct data that he provided.
        coupon = self.get_coupon(note="my first coupon")
        old_coupons = self.get('coupons/').json()
        self.post('coupons/', json=coupon)
        new_coupons = self.get('coupons/').json()
        self.assertGreater(len(new_coupons), len(old_coupons))

    def test_post_coupon_multiple_odds_bookmaker_mixed(self):
        # The he decided to make a new coupon with multiple bet in it but he
        # forgot the golden rule: "do not mix bookmakers odds".
        # The api return error with message explanation
        expected_msg = {'bets': [
            'Can\'t create coupon with odds from differnt bookmakers']}
        odd_1 = self.get_coupon(bookmaker='888sport')['bets'][0]
        odd_2 = self.get_coupon(bookmaker='bwin')['bets'][0]
        coupon = {'bets': [odd_1, odd_2], 'money': 10, 'note': ''}
        request = self.post('coupons/', json=coupon)
        self.assertEqual(request.json(), expected_msg)

    def test_post_coupon_multiple_odds_same_odds(self):
        # Another mistake make by Sam
        expected_msg = {'bets': [
            'Can\'t create coupon with due to odds repetitions']}
        odd = self.get_coupon()['bets'][0]
        coupon = {'bets': [odd, odd], 'money': 10, 'note': ''}
        request = self.post('coupons/', json=coupon)
        self.assertEqual(request.json(), expected_msg)

    def test_post_coupon_multiple_odds(self):
        # Sam try again to save a coupon with multiple odds and this time
        # all goes well but never the less he check the coupon page.
        expected_msg = {'money': 10.0, 'note': '', 'status': None}
        odd_1 = self.get_coupon(event=0)['bets'][0]
        odd_2 = self.get_coupon(event=1)['bets'][0]
        coupon = {'bets': [odd_1, odd_2], 'money': 10, 'note': ''}
        request = self.post('coupons/', json=coupon)
        self.assertEqual(request.status_code, 201)
        self.assertDictContainsSubset(expected_msg, request.json())

    def test_delete_coupon(self):
        # Sam now wants to delete an old coupon
        coupons = self.get('coupons/').json()
        coupon_deleted = coupons[0]
        self.delete(f'coupons/{coupon_deleted["id"]}')
        coupons_remaning = self.get('coupons/').json()
        self.assertNotIn(coupon_deleted, coupons_remaning)

# After test all the functionality of the aao-api he decided to use it to
# develope new betting strategies.
