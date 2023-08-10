from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, TokenObtainPairSerializer
from rest_framework import viewsets, status


'''class RegisterView(APIView):
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            user = get_user_model().objects.create_user(**serializer.validated_data)
            message = 'User created successfully.'
            return Response(status=HTTP_201_CREATED, data={'message': message, 'user_id': user.id})
        return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})'''

class RegisterView(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.create_user(**serializer.validated_data)
            message = 'User created successfully.'
            return Response(status=status.HTTP_201_CREATED, data={'message': message, 'user_id': user.id})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
