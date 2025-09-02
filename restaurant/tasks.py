from celery import shared_task
from django.utils import timezone
from datetime import timedelta, time, datetime
from .models import Reservation


@shared_task
def change_reservation_status():
    reservations = Reservation.objects.filter(status__in=['created', 'active'])
    for reservation in reservations:
        if (reservation.status == 'created' and
                reservation.start_time <= datetime.now() and
                reservation.end_time > datetime.now()):
            reservation.status = 'active'
        elif reservation.end_time <= datetime.now():
            reservation.status = 'completed'
