import random

from django.db import transaction
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from leef.models import User, Token
from leef.serializer import UserSerializer


class UserCreateAPIView(ListModelMixin, GenericAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        if not self.validate_token(token):
            return Response({'message': '로그인이 필요합니다.'}, status=401)
        return super().list(request, *args, **kwargs)

    def validate_token(self, token):
        valid_token = "your_secret_token"
        return token == valid_token

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(**serializer.validated_data)
        return_data = self.get_serializer(user).data
        return Response(return_data, status=201)


class UserDetailAPIView(APIView):
    def get(self, request, user_id):
        user: User = get_object_or_404(User, id=user_id)
        return_data = UserSerializer(user).data
        return Response(return_data, status=200)

    def put(self, request, user_id):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            from leef.models import User
            user: User = get_object_or_404(User, id=user_id)
            user.name = request.data["name"]
            user.nickname = request.data["nickname"]
            user.password = request.data["password"]
            user.save()
            return_data = UserSerializer(user).data
            return Response(return_data, status=200)

    def delete(self, request, user_id):
        from leef.models import User
        get_object_or_404(User, id=user_id).delete()
        return Response(status=204)


class SignupAPIView(APIView):
    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')

        if not name or not password:
            return Response(status=401)

        if User.objects.filter(name=name).exists():
            return Response(data={'존재하는 이름입니다..'}, status=401)

        with transaction.atomic():
            new_user = User.objects.create(name=name, password=password)

            if new_user:
                token = Token.objects.create(user=new_user, key=new_user.name)
                return Response(data={'token': token.key}, status=201)

            else:
                return Response(status=500)


class TokenVerificationAPIView(APIView):
    def get(self, request):
        token_key = request.query_params['token']

        try:
            token = Token.objects.get(key=token_key)
            return Response(data={'성공'}, status=200)
        except Token.DoesNotExist:
            return Response(data={'실패'}, status=401)


class LoginAPIView(APIView):
    def post(self, request):
        name = request.data['name']
        password = request.data['password']

        if not User.objects.filter(name=name).exists():
            return Response(status=401)

        user = User.objects.get(name=name)
        if user.password == password:
            token, created = Token.objects.get_or_create(user=user, defaults={'key': random.random()})
            return Response(data={'token': token.key}, status=200)

        else:
            return Response(status=401)


class LogoutAPIView(APIView):
    def delete(self, request):
        token = request.data.get('token')
        if token:
            Token.objects.filter(key=token).delete()
            return Response(status=204)
        return Response(status=404)
