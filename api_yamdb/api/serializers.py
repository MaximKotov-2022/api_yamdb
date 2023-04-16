from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Category, Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    category=SlugRelatedField(
    slug_field='slug',
    queryset=Category.objects.all()
    )
    genre=SlugRelatedField(
    slug_field='slug',
    queryset=Genre.objects.all(),
    many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

