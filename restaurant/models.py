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
    STATUS_CHOICES = [("created","Ожидает подтверждения"), ("active", "Активна"), ("completed", "Завершена")]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    time = models.TimeField(auto_now_add=False)
    reserve_time = models.IntegerField(default=1)
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
