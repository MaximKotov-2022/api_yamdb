import datetime
from django.conf import settings
from rest_framework import serializers
from reviews.models import (Category, Genre, Title, Comment,
                            GenreTitle, Review,
                            )
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        required=True,
        max_length=settings.USERNAME_MAX_LENGTH
    )
    email = serializers.EmailField(
        max_length=settings.EMAIL_MAX_LENGTH,
        required=True,
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Недопустимый псевдоним "me"')
        return value

    def validate(self, value):
        username = value['username']
        email = value['email']
        if (User.objects.filter(
                email=email
        ).exclude(
            username=username
        ).exists() or User.objects.filter(
            username=username
        ).exclude(email=email).exists()):
            raise serializers.ValidationError({'email': 'Имя занято'})
        return value

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH
    )
    confirmation_code = serializers.CharField(
        max_length=settings.CONFIRMATION_CODE_MAX_LENGTH
    )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    genre = GenreSerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class TitlesCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    def validate_year(self, value):
        year = datetime.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год издания.')
        return value

    def create(self, validated_data):
        category = validated_data.pop('category')
        genres = validated_data.pop('genre')

        title = Title.objects.create(**validated_data, category=category)

        for genre in genres:
            genre = Genre.objects.get(slug=genre.slug)
            GenreTitle.objects.create(genre=genre, title=title)
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get(
            'description', instance.description)

        category = validated_data.pop('category')
        instance.category = validated_data.get('category', category)

        title = Title.objects.get(pk=instance.id)
        if 'genre' in validated_data:
            genres = validated_data.pop('genre')
            for genre in genres:
                genre = Genre.objects.get(slug=genre.slug)
                GenreTitle.objects.create(genre=genre, title=title)

        instance.save()

        return instance

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def create(self, validated_data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title=validated_data.get('title')
        ).exists():
            raise serializers.ValidationError(
                'Нельзя оставить больше одного обзора.')

        return Review.objects.create(**validated_data,)

    class Meta:
        model = Review
        exclude = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        exclude = ('review',)
