from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

ROLE_USER_ID = 1
ROLES = [
    (ROLE_USER_ID, 'user'),
    (2, 'moderator'),
    (3, 'admin'),
]


class User(AbstractUser):
    username_validator = RegexValidator(r'^[\w.@+-]+\z')
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator]
    )
    email = models.EmailField('Почта', max_length=254, blank=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=None,
        default=ROLE_USER_ID,
        choices=ROLES
    )
