from datetime import timedelta, datetime

from django.db import models
from django.utils import timezone

from users.models import User


# Create your models here.
class Contacts(models.Model):
    mobile_phone_number = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=20)
    subway = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.mobile_phone_number} | {self.phone_number} | {self.email} | {self.city} | {self.subway} | {self.address}"

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"


class Content(models.Model):
    CONTENT_TYPE_CHOICES = [("carousel", "Карусель"),
                            ("promotions", "Акции"),
                            ("services", "Услуги"),
                            ("team", "Команда"),
                            ("mission", "Миссия ресторана"),
                            ("history", "История ресторана"),
                            ("contacts", "Контакты"),
                            ("news", "Новости"),
                            ("description", "Описание ресторана")]

    title = models.CharField(max_length=100)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='img/content/', blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    content_type = models.CharField(max_length=100, choices=CONTENT_TYPE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"
        ordering = ['title']


class Table(models.Model):
    '''Модель столика'''
    number = models.IntegerField(unique=True)
    seats = models.IntegerField()
    hall = models.CharField(max_length=20, choices=(
        ('main', 'Основной зал'),
        ('vip', 'VIP зал'),
    ))
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Стол №{self.number} ({self.seats} мест, {self.get_hall_display()})"

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        ordering = ["number"]


class Reservation(models.Model):
    '''Модель брони столика'''
    STATUS_CHOICES = [("created","Ожидает подтверждения"), ("active", "Активна"), ("completed", "Завершена"), ("cancelled", "Отменена"),]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(blank=True, null=True, max_length=100)
    last_name = models.CharField(blank=True, null=True, max_length=100)
    date = models.DateField(auto_now_add=False)
    start_time = models.TimeField(auto_now_add=False, null=True, blank=True)
    duration = models.IntegerField(default=1)
    end_time = models.TimeField(editable=False, null=True, blank=True)  # вычисляемое поле

    def get_end_time(self):
        """Возвращает время окончания"""
        if self.start_time and self.duration:
            # Создаем фиктивную дату и добавляем часы
            dummy_datetime = datetime.combine(datetime.today(), self.start_time)
            end_datetime = dummy_datetime + timedelta(hours=self.duration)
            return end_datetime.time()
        return None

    def save(self, *args, **kwargs):
        # Вычисляем время окончания перед сохранением
        self.first_name = self.user.first_name
        self.last_name = self.user.last_name
        if self.start_time and self.duration:
            dummy_datetime = datetime.combine(datetime.today(), self.start_time)
            end_datetime = dummy_datetime + timedelta(hours=self.duration)
            self.end_time = end_datetime.time()
        super().save(*args, **kwargs)

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    celebration = models.BooleanField(default=False)
    guests = models.IntegerField(default=1)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="created")


    def __str__(self):
        return f"Стол: {self.table.number} | Дата: {self.date} | Гость: {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
        ordering = ["date"]
