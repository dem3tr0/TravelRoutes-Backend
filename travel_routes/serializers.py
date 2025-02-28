from rest_framework import serializers
from .models import Route, Review, Photo

# Для истории маршрутов
Route_History = Route.history.model

# Сериализатор для фотографий
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'route_id']

# Основной сериализатор маршрутов
class RouteSerializer(serializers.ModelSerializer):
    points = serializers.JSONField()  # Обрабатываем JSON

    class Meta:
        model = Route
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True}  # Пользователь устанавливается автоматически
        }

    def create(self, validated_data):
        # Создаем маршрут
        return Route.objects.create(**validated_data)

# Сериализатор для истории изменений маршрутов
class RouteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Route_History
        fields = '__all__'

# Сериализатор для отзывов
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'