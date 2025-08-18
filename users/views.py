from django.contrib.auth.views import LoginView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.permissions import IsStaff, IsCurrentUser
from users.serializers import UserSerializer


# Create your views here.
class LoginUserView(LoginView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    template = "users/login.html"


class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    template = "register.html"
    serializer_class = UserSerializer


class ListUserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    template = "list.html"
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsStaff)


class RetriveUserAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    template = "profile.html"
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsCurrentUser)


class UpdateUserAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    template = "update.html"
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsCurrentUser)


class DeleteUserAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    template = "delete.html"
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsCurrentUser)

