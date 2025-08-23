
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView, DetailView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse_lazy

from restaurant.models import Reservation
from users.models import User
from users.permissions import IsStaff, IsCurrentUser
from users.serializers import UserSerializer


# Create your views here.
class LoginUserView(LoginView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    template = "html/login.html"


class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    template = "html/register.html"
    serializer_class = UserSerializer


class ListUserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    template = "html/list.html"
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsStaff)


class ProfileView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("users:login")
    template_name = "html/profile.html"
    permission_classes = (IsCurrentUser, )
    queryset = Reservation.objects.all()
    context_object_name = "reservations"

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class UpdateUserAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    template_name = "html/update.html"
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsCurrentUser)


class DeleteUserAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    template = "html/delete.html"
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsCurrentUser)


class UserReservationView(DetailView):
    template_name = "html/reservation_detail.html"
    permission_classes = (IsAuthenticated, IsCurrentUser)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

