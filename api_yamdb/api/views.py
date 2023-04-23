from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)

from api.permissions import IsAdminOrReadOnly
from api.serializers import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre, Review, Title

from .filters import TitlesFilter
from .mixins import ListCreateDeleteMixin, TitleReviewCommentViewSet
from .permissions import (IsAdminPermission, IsAuthorPermission,
                          IsReadOnlyPermission)
from .serializers import (CommentSerializer, ReviewSerializer,
                          TitlesCreateUpdateSerializer, TitlesSerializer)


class TitlesViewSet(TitleReviewCommentViewSet):
    permission_classes = [IsReadOnlyPermission | IsAdminPermission]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitlesCreateUpdateSerializer

        return TitlesSerializer


class ReviewViewSet(TitleReviewCommentViewSet):
    permission_classes = IsAuthorPermission,
    pagination_class = PageNumberPagination
    serializer_class = ReviewSerializer

    def check_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.check_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.check_title())


class CategoryViewSet(ListCreateDeleteMixin):
    '''Категории.'''
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDeleteMixin):
    '''Жанры.'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class CommentViewSet(TitleReviewCommentViewSet):
    permission_classes = IsAuthorPermission,
    pagination_class = PageNumberPagination
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"),)

        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"),)
        serializer.save(author=self.request.user, review=review)
