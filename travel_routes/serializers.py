from rest_framework import serializers
from .models import Route, Review, Photo, Likes

# Для истории маршрутов
Route_History = Route.history.model

# Сериализатор для фотографий
class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image', 'route_id']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

# Основной сериализатор маршрутов
class RouteSerializer(serializers.ModelSerializer):
    points = serializers.JSONField()  # Обрабатываем JSON
    photos = serializers.SerializerMethodField()  # Добавляем поле для фотографий

    class Meta:
        model = Route
        fields = ['id', 'title', 'description', 'points', 'is_private', 'photos']
        extra_kwargs = {
            'user_id': {'read_only': True}  # Пользователь устанавливается автоматически
        }

    def get_photos(self, obj):
        photos = obj.photos.all()  # Получаем все фотографии маршрута
        return PhotoSerializer(photos, many=True, context=self.context).data

    def create(self, validated_data):
        # Устанавливаем текущего пользователя как создателя маршрута
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)

# Сериализатор для истории изменений маршрутов
class RouteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Route_History
        fields = '__all__'

# Сериализатор для отзывов
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'rating', 'user_id', 'route_id', 'created_at']
        extra_kwargs = {
            'user_id': {'read_only': True},  # Запрещаем передачу user_id из запроса
            'route_id': {'read_only': True},  # Запрещаем передачу route_id из запроса
        }

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5")
        return value

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['id', 'user_id', 'route_id']