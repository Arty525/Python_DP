from datetime import timedelta

from django.utils import timezone
from rest_framework.exceptions import ValidationError


class ReservationDateValidator:
    def __init__(self, field):
        self.date = field

    def __call__(self, fields):
        now_date = timezone.localtime(timezone.now()).date()
        if fields["date"].date() < now_date:
            raise ValidationError("Невозможно забронировать столик на эту дату")


class ReservationTimeValidator:
    def __init__(self, field):
        self.time = field

    def __call__(self, fields):
        now_time = timezone.localtime(timezone.now()).time()
        if fields["time"].time() < now_time:
            raise ValidationError("Невозможно забронировать столик на это время")


class ReservationGuestsValidator:
    def __init__(self, field):
        self.guests = field

    def __call__(self, fields):
        if fields["guests"] < 1:
            raise ValidationError("Число гостей не может быть меньше 1")


