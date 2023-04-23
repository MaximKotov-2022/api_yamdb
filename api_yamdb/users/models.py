from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    ROLE_CHOICES_MAX_LENGTH = max(len(choice[0]) for choice in ROLE_CHOICES)
    email = models.EmailField(
        'Электронная почта',
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True
    )
    role = models.CharField(
        'Роль',
        max_length=ROLE_CHOICES_MAX_LENGTH,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        'Биография', blank=True
    )

    @property
    def is_admin(self):
        """Проверка пользователя на наличие прав администратора."""
        return self.role in [self.ADMIN, self.is_superuser]

    @property
    def is_moderator(self):
        """Проверка пользователя на наличие прав модератора."""
        return self.role in [self.MODERATOR, self.ADMIN, self.is_superuser]

    @property
    def is_user(self):
        """Проверка пользователя на наличие стандартных прав."""
        return self.role in [self.USER]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('username', 'email'),
                                    name='unique_username_email')
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', )
