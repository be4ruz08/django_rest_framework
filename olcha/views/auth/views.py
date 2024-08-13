from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from olcha.serializers import LoginSerializer, RegisterSerializer


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "username": {
                    "detail": "User does not exist!"
                }
            }
            if User.objects.filter(username=request.data["username"]).exists():
                user = User.objects.get(username=request.data["username"])
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                    'token': token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(
            {
                'success': True,
                'message': 'Successfully logged out.',
            },
            status=status.HTTP_200_OK,
        )


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kargs):
        serializer = RegisterSerializer(data=request.data)
        # user = User.objects.get(username=serializer.data.get('username'))
        # token = Token.objects.get(user=user).key
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'success': True,
                    'username': User.objects.get(username=serializer.data.get('username')).username,
                    'message': 'Successfully registered.',
                    'token': Token.objects.get(user=User.objects.get(username=serializer.data['username'])).key
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
