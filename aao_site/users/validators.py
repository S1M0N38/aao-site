from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError(
            _(f'A user with that email already exists.'),
            code='invalid'
        )
