from django.utils import timezone
from rest_framework import status
from app.settings import SECRET_KEY
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
from django.db.models import Q
import datetime
import jwt
from django.conf import settings

class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        identifier = request.data['identifier']
        password = request.data['password']

        if not identifier or not password:
            return Response({'error': 'Missing email/username or password'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(Q(email=identifier) | Q(username=identifier)).first()

        if not user:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')

        payload = {
            'id': user.id,
            'exp': timezone.now() + datetime.timedelta(minutes=60),
            'iat': timezone.now()
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        response = Response()
        response.set_cookie('token', value=token, httponly=True)
        response.data = {
            'token': token,
            'userId': user.id,
        }

        return response


class UserView(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthorized')

        token = auth_header.split(' ')[1]
        print(f"Received token: {token}")  # Логирование токена

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            print(f"Decoded payload: {payload}")  # Логирование декодированного payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            raise AuthenticationFailed('User not found')

        serializer = UserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'message': 'Logged out',
        }
        return response