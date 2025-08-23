from django.db import models

from users.models import User


# Create your models here.

class Content(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField(upload_to='media/img/content/', blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"
        ordering = ['title']


class Table(models.Model):
    '''Модель столика'''
    HALL_CHOICES = ["Общий зал", "VIP-Зал"]
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
    STATUS_CHOICES = ("Ожидает подтверждения", "Активна", "Завершена")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    time = models.TimeField(auto_now_add=False)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    celebration = models.BooleanField(default=False)
    guests = models.IntegerField(default=1)
    status = models.CharField(max_length=100, default="Ожидает подтверждения")


    def __str__(self):
        return f"Стол: {self.table.number} | Дата: {self.date} | Гость: {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
        ordering = ["date"]
