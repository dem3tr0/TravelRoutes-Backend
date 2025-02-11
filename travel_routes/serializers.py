from rest_framework import serializers
from .models import Route, Review

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        """
        # При вызове сериализатора для уникального маршрута, нам не нужно получать

        """
        model = Route
        fields = [
            'user_id',
            'title',
            'description',
            'is_private',
            'created_at',
            'updated_at',
            'points',
        ]

class RouteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'