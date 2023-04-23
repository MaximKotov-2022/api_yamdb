import datetime
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import (Category, Genre, Title, Comment,
                            Review,
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
        lookup_field = 'slug',


class TitlesSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)
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
        required=True,
    )

    def validate_year(self, value):
        year = datetime.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год издания.')
        return value

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, obj):
        title_id = self.context['view'].kwargs.get('title_id')
        request = self.context['request']
        title = get_object_or_404(Title, id=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                author=request.user, title=title
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили свое ревью к этому тайтлу'
                )
        return obj


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
