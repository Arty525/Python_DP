import os
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView, CreateView, DeleteView, UpdateView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse_lazy
from restaurant.models import Reservation
from users.forms import PasswordChangeForm, PasswordRecoveryRequestForm, CustomUserCreationForm, CustomUserLoginForm, \
    CustomUserUpdateForm
from users.models import User


# Create your views here.
class LoginUserView(LoginView):
    template_name = "html/login.html"
    form_class = CustomUserLoginForm
    def get_success_url(self):
        return reverse_lazy('restaurant:home_page')


class CreateUserView(CreateView):
    queryset = User.objects.all()
    template_name = "html/register.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.is_active = False
        user.save()

        self.assign_limited_permissions(user)

        self.send_verification_email(user, form.cleaned_data.get("email"))

        return super().form_valid(form)

    def assign_limited_permissions(self, user):
        if user.is_staff or user.is_superuser:
            return

        limited_group, created = Group.objects.get_or_create(name='Limited Users')
        if created:
            self.setup_limited_group_permissions(limited_group)

        user.groups.add(limited_group)
        user.save()

    def setup_limited_group_permissions(self, group):
        reservation_content_type = ContentType.objects.get_for_model(Reservation)
        reservation_perms = Permission.objects.filter(
            content_type=reservation_content_type,
            codename__in=['view_reservation', 'add_reservation', 'change_reservation', 'delete_reservation']
        )

        user_content_type = ContentType.objects.get_for_model(User)
        user_perms = Permission.objects.filter(
            content_type=user_content_type,
            codename__in=['view_user', 'change_user']
        )

        all_perms = list(reservation_perms) + list(user_perms)
        group.permissions.set(all_perms)
        group.save()

    def send_verification_email(self, user, email):
        print('ПИСЬМО ОТПРАВЛЕНО')
        verification_url = reverse_lazy("users:verify_email", kwargs={"pk": user.pk})
        absolute_url = self.request.build_absolute_uri(verification_url)

        send_mail(
            subject="Регистрация на сайте",
            message=f"""Здравствуйте!
    Вы зарегистрировались на сайте.
    Для подтверждения email перейдите по ссылке:
    {absolute_url}

    Ваши права на сайте ограничены: вы можете создавать и просматривать свои резервирования, а также редактировать свой профиль.""",
            from_email=os.getenv("EMAIL_HOST_USER"),
            recipient_list=[email],
        )

class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    template_name = "html/list.html"
    permission_classes = (IsAuthenticated,)


class UserDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy("users:login")
    template_name = "html/profile.html"
    queryset = User.objects.all()
    context_object_name = "reservations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        context['reservations'] = Reservation.objects.filter(user=self.kwargs.get('pk'))
        return context


class UpdateUserView(UpdateView):
    queryset = User.objects.all()
    template_name = "html/update.html"
    permission_classes = (IsAuthenticated,)
    form_class = CustomUserUpdateForm
    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})


class DeleteUserView(DeleteView):
    queryset = User.objects.all()
    template_name = "html/delete.html"
    permission_classes = (IsAuthenticated,)


class UserReservationView(DetailView):
    template_name = "html/reservation_detail.html"
    permission_classes = (IsAuthenticated,)
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
