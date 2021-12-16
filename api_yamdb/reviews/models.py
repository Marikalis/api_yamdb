from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

ROLE_USER_ID = 1
ROLES = [
    (ROLE_USER_ID, 'user'),
    (2, 'moderator'),
    (3, 'admin'),
]

# class Activation(models.Model):
#     username = models.CharField(
#         max_length=150,
#         unique=True,
#         validators=[username_validator]
#     )


class User(AbstractUser):
    username_validator = RegexValidator(r'^[\w.@+-]+\z')
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator]
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        blank=True
    )
    password = None
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=150,
        default=ROLE_USER_ID,
        choices=ROLES
    )
    REQUIRED_FIELDS = ['email']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'