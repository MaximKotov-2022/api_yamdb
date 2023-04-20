from django.db import models

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
        max_length=256,
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
