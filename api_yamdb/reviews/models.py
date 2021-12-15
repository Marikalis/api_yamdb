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


class AnonymousUser(User):
    id = None
    pk = None
    username = ''
    is_staff = False
    is_active = False
    is_superuser = False

    def __str__(self):
        return 'AnonymousUser'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __hash__(self):
        return 1  # instances always return the same hash value

    def __int__(self):
        raise TypeError()

    def save(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def set_password(self, raw_password):
        raise NotImplementedError()

    def check_password(self, raw_password):
        raise NotImplementedError()
