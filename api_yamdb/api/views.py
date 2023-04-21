from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from api.permissions import IsAdminOrReadOnly
from api.serializers import (CategorySerializer, GenreSerializer)
from reviews.models import Category, Genre, Title, Review
from users.models import User
from django.db.models import Avg
from .permissions import (IsAdminOrSuperuser, IsAdminPermission,
                          IsAuthorPermission, IsReadOnlyPermission,
                          )
from .serializers import (SignUpSerializer, TokenSerializer, UserSerializer,
                          TitlesCreateUpdateSerializer, TitlesSerializer,
                          ReviewSerializer, CommentSerializer,
                          )
from .filters import TitlesFilter
from .mixins import ListCreateDeleteMixin, TitleReviewCommentViewSet


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet модели User."""
    queryset = User.objects.all()
    permission_classes = (IsAdminOrSuperuser,)
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]
    lookup_field = 'username'
    http_method_names = ['get', 'patch', 'delete', 'post']

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated, ),
    )
    def me(self, request):
        """Получение данных своей учётной записи."""
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserSerializer(
            request.user, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """Создание нового пользователя."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user, created = User.objects.get_or_create(username=username, email=email)
    token = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {token}',
        settings.MAILING_EMAIL,
        [email],
        fail_silently=False,
    )
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_token(request):
    """Создание JWT-токена для пользователей."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    confirmation_code = serializer.validated_data.get('confirmation_code')
    token = default_token_generator.check_token(user, confirmation_code)

    if default_token_generator.check_token(
       user, serializer.data['confirmation_code']):
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK)
    return Response({
        'confirmation code': 'Некорректный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST)


class TitlesViewSet(TitleReviewCommentViewSet):
    permission_classes = [IsReadOnlyPermission | IsAdminPermission]
    pagination_class = PageNumberPagination
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitlesCreateUpdateSerializer

        return TitlesSerializer

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return Title.objects.annotate(rating=Avg('reviews__score'))

        return Title.objects.all()

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return Title.objects.annotate(rating=Avg('reviews__score'))

        return Title.objects.all()


class ReviewViewSet(TitleReviewCommentViewSet):
    permission_classes = IsAuthorPermission,
    pagination_class = PageNumberPagination
    serializer_class = ReviewSerializer

    def check_title(self):
        title_id = self.kwargs.get("title_id")

        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        title = self.check_title()

        return title.reviews.all()

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
    pagination_class = LimitOffsetPagination
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
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)

        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
