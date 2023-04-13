from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    username = models.SlugField(
        'Имя пользователя',
        max_length=200,
        blank=False,
        unique=True
    )
    email = models.EmailField(
        'Почта',
        blank=False,
        unique=True,
    )
    role = models.CharField(
        'Роль',
        max_length=200,
        choices=USER_ROLES,
        default='user',
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    def __str__(self):
        return self.username
