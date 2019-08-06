from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator


class Event(models.Model):
    datetime = models.DateTimeField()
    country = models.CharField(max_length=100)
    league = models.CharField(max_length=100)
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    home_goals = models.IntegerField(null=True)
    away_goals = models.IntegerField(null=True)

    class Meta:
        db_table = 'api_events'
        ordering = ('datetime',)

    def __str__(self):
        return f'{self.home_team} v {self.away_team}'


class Odd(models.Model):
    BOOKMAKERS = (
        ('bet365', 'bet365'),
        ('bwin', 'bwin'),
        ('888sport', '888sport'),
        ('williamhill', 'williamhill'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    bookmaker = models.CharField(max_length=15, choices=BOOKMAKERS)
    full_time_result = JSONField(null=True)
    draw_no_bet = JSONField(null=True)
    both_teams_to_score = JSONField(null=True)
    double_chance = JSONField(null=True)
    under_over = JSONField(null=True)

    class Meta:
        abstract = True
        ordering = ('datetime',)

    def __str__(self):
        return f'{self.bookmaker} - {self.event}'


class ActiveOdd(Odd):
    class Meta:
        db_table = 'api_active_odds'
        default_related_name = 'odds'


class AllOdd(Odd):
    class Meta:
        db_table = 'api_all_odds'
        default_related_name = 'all_odds'


class Coupon(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    money = models.FloatField(validators=[MinValueValidator(0)])
    note = models.TextField(default='', blank=True)
    status = models.NullBooleanField()

    class Meta:
        db_table = 'api_coupons'

    def __str__(self):
        return f'{self.user} - {self.id}'


class Bet(models.Model):
    TYPES = (
        ('full_time_result', 'full_time_result'),
        ('draw_no_bet', 'draw_no_bet'),
        ('both_teams_to_score', 'both_teams_to_score'),
        ('double_chance', 'double_chance'),
        ('under_over', 'under_over'),
    )
    VALUES = (('1', '1'), ('X', 'X'), ('2', '2'), ('12', '12'), ('1X', '1X'),
              ('X2', 'X2'), ('over', 'over'), ('under', 'under'),
              ('yes', 'yes'), ('no', 'no'))
    odd = models.ForeignKey(AllOdd, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPES)
    option = models.CharField(max_length=5, choices=VALUES)
    value = models.FloatField(default=None, null=True)
    status = models.NullBooleanField()

    class Meta:
        db_table = 'api_bets'
        default_related_name = 'bets'

    def save(self, *args, **kwargs):
        """
        Save the current value for the odds. Theoretically it's already store
        in the odd link to the bet but it's also useful to store it here
        in order to perform some simple calulation later.
        """
        value = getattr(self.odd, self.type)[self.option]
        self.value = value
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.odd} - {self.type} - {self.option}'
