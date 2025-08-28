import os

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse_lazy

from restaurant.models import Reservation
from users.forms import PasswordChangeForm, PasswordRecoveryRequestForm
from users.models import User
from users.permissions import IsStaff, IsCurrentUser
from users.serializers import UserSerializer


# Create your views here.
class LoginUserView(LoginView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    template_name = "html/login.html"


class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    template_name = "html/register.html"
    serializer_class = UserSerializer


class ListUserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    template_name = "html/list.html"
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
    template_name = "html/delete.html"
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsCurrentUser)


class UserReservationView(DetailView):
    template_name = "html/reservation_detail.html"
    permission_classes = (IsAuthenticated, IsCurrentUser)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class VerifyEmailView(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        user.is_active = True
        user.save()
        return redirect(reverse_lazy("users:success_verify"))


class SuccessVerifyView(TemplateView):
    template_name = "html/success_verify.html"


class PasswordRecoveryRequestView(FormView):
    model = User
    template_name = "html/password_recovery_request.html"
    form_class = PasswordRecoveryRequestForm
    success_url = reverse_lazy("users:password_recovery_request_success")

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        user_pk = get_object_or_404(User, email=email)
        recovery_url = reverse_lazy("users:password_change", kwargs={"pk": user_pk.pk})
        absolute_url = self.request.build_absolute_uri(recovery_url)

        send_mail(
            subject="Восстановление пароля",
            message=f"""Для восстановления пароля пройдите по ссылке:
{absolute_url}
Если вы не запрашивали восстановление пароля, то проигнорируйте это письмо""",
            from_email=os.getenv("EMAIL_HOST_USER"),
            recipient_list=[email],
        )
        return redirect(reverse_lazy("users:password_recovery_request_success"))


class PassRecoveryRequsetSuccess(TemplateView):
    template_name = "html/password_recovery_request_success.html"


class PasswordChangeView(FormView):
    model = User
    template_name = "html/password_recovery.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("users:login")

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        print(user.email)
        user.set_password(request.POST.get("password1"))
        user.save()
        update_session_auth_hash(request, user)
        return redirect(reverse_lazy("users:login"))


class ChangeUserStatus(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:login")

    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)
        if request.user.has_perm("sender.can_ban") and not user.is_superuser:
            user.is_banned = not user.is_banned
            user.save()
            if user.is_banned:
                email = user.email
                send_mail(
                    subject="Ваша учетная запись заблокирована",
                    message=f"Здравствуйте, {user.username}! К сожалению Ваша учетная запись была заблокирована.",
                    from_email=os.getenv("EMAIL_HOST_USER"),
                    recipient_list=[email],
                )
            return redirect(reverse_lazy("users:user_list"))
        return HttpResponseForbidden("У вас нет прав для блокировки этого пользователя")


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("restaurant:home_page")
