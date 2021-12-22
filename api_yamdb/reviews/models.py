from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
]


class User(AbstractUser):
    username_validator = RegexValidator(r'^[\w.@+-]+')
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator]
    )
    email = models.EmailField(
        'Почта',
        unique=True,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        max_length=256,
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=30,
        default=USER,
        choices=ROLES
    )
    password = None

    REQUIRED_FIELDS = ['email']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
