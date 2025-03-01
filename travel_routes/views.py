from rest_framework import viewsets, parsers, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import ValidationError, AuthenticationFailed
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Route, Review, Photo, Likes
from .serializers import (
    RouteSerializer,
    ReviewSerializer,
    RouteHistorySerializer,
    PhotoSerializer
)

User = get_user_model()


class JWTAuthentication:
    """
    Кастомная аутентификация с использованием JWT.
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('id')
            user = User.objects.get(id=user_id)
            return (user, None)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

    def authenticate_header(self, request):
        """
        Возвращает строку для заголовка WWW-Authenticate.
        """
        return 'Bearer realm="api"'


class IsAuthenticated(BasePermission):
    """
    Кастомное разрешение для проверки аутентификации.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]  # Добавляем поддержку FormData

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя как создателя маршрута
        serializer.save(user_id=self.request.user)

        # Сохраняем фотографии, если они есть
        photos = self.request.FILES.getlist('photos')
        for photo in photos:
            Photo.objects.create(route_id=serializer.instance, image=photo)


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def perform_create(self, serializer):
        # Получаем объект Route по его ID
        route_id = self.request.data.get('route_id')
        route = Route.objects.get(id=route_id)
        # Сохраняем фото и связываем его с маршрутом
        serializer.save(route_id=route)


class RouteHistoryViewSet(viewsets.ModelViewSet):
    """
    История изменений маршрутов.
    """
    authentication_classes = [JWTAuthentication]  # Используем кастомную аутентификацию
    permission_classes = [IsAuthenticated]  # Используем кастомное разрешение
    queryset = Route.objects.all()
    serializer_class = RouteHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id']  # Фильтрация по user_id


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(
            user_id=self.request.user,
            route_id=Route.objects.get(id=self.kwargs['routeId'])
        )

    def get_queryset(self):
        route_id = self.kwargs.get('route_id')
        return Review.objects.filter(route_id=route_id)

class LikeView(APIView):
    def post(self, request, route_id):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)


        like = Likes.objects.filter(user_id=user, route_id=route_id).first()
        if like:
            like.delete() 
            return Response({"message": "Лайк удален"}, status=status.HTTP_200_OK)

        like = Likes(user_id=user, route_id_id=route_id)
        like.save()
        return Response({"message": "Лайк добавлен"}, status=status.HTTP_201_CREATED)

    def get(self, request, route_id):
        likes_count = Likes.objects.filter(route_id=route_id).count()
        return Response({"likes_count": likes_count}, status=status.HTTP_200_OK)