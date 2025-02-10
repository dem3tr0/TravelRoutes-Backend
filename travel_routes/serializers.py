from rest_framework import serializers
from .models import Route, Review

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class RouteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'