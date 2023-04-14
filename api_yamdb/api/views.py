from rest_framework import viewsets

from reviews.models import Category, Genre, Title


class TitleViewSet(viewsets.ModelViewSet):
    '''Произведения.'''
    queryset = Title.objects.all()
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    '''Категории.'''
    queryset = Category.objects.all()
    pass


class GenreViewSet(viewsets.ModelViewSet):
    '''Жанры.'''
    queryset = Genre.objects.all()
    pass