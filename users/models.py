from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    # Для устранения ошибки при создании пользователя без username
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    '''Модель пользователя'''
    username = None
    email = models.EmailField(unique=True, verbose_name="E-mail")
    first_name = models.CharField(
        max_length=50, verbose_name="Имя", null=True, blank=True
    )
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия", null=True, blank=True
    )
    phone_number = models.CharField(
        max_length=50, verbose_name="Номер телефона", null=True, blank=True
    )
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} - {self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]


class Table(models.Model):
    '''Модель столика'''
    number = models.IntegerField()
    status = models.BooleanField(default=True)
    hall = models.CharField(max_length=100)
    seats = models.IntegerField()

    def __str__(self):
        status = "Свободен"
        if not self.status:
            status = "Забронирован"
        return f"Номер: {self.number} | Зал: {self.hall} | Статус: {status} | Число мест: {self.seats}"

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        ordering = ["number"]


class Reservation(models.Model):
    '''Модель брони столика'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=False)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, blank=True, null=True)
    celebration = models.BooleanField(default=False)
    guests = models.IntegerField(default=1)


    def __str__(self):
        return f"Стол: {self.table.number} | Дата: {self.date} | Гость: {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
        ordering = ["date"]
