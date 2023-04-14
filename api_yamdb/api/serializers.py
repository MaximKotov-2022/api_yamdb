from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True,
    )
    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    ...