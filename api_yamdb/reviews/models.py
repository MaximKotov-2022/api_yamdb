from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import validate_year


class Category(models.Model):
    '''Категории.'''
    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.slug[:10]


class Genre(models.Model):
    '''Жанры'''
    name = models.CharField(max_length=256,)
    slug = models.SlugField(max_length=50, unique=True,)

    def __str__(self) -> str:
        return self.slug[:10]


class Title(models.Model):
    '''Произведения.'''
    name = models.CharField(
        max_length=100,
        db_index=True,
    )
    year = models.IntegerField(
        db_index=True,
        validators=[validate_year],
    )

    category = models.ForeignKey(
        'Category',
        related_name='titles',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        db_index=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name[:10]


class GenreTitle(models.Model):
    '''Присвоение произведению жанра.'''
    title = models.ForeignKey(Title, on_delete=models.CASCADE,)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,)

    def __str__(self) -> str:
        return f'{self.title},{self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(
        verbose_name='Текст обзора',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор обзора',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации обзора',
    )
    score = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Оценка произведения',
    )

    class Meta:
        verbose_name = 'обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='one_review_per_title'
            )
        ]

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор на произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.author.username + '_' + self.text[:10]
