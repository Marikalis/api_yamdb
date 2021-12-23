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

SCORES = [ (i, i) for i in range (1, 11)]


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


class Rewiew(models.Model):
    title = models.ForeignKey(
        Title,
        'Произведение'
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        'Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
        db_column='author')
    score = models.IntegerField(
        'Оценка',
        choices=SCORES)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'],
            name='unique author review')]

class Comment(models.Model):
    rewiew = models.ForeignKey(
        Rewiew,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        db_column='author')
    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        db_table = 'comments'
