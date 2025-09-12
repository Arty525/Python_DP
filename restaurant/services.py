from datetime import datetime, timedelta
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST
from restaurant.models import Reservation, Table


@require_GET
def get_free_tables(request):
    date = request.GET.get('date')
    time_str = request.GET.get('time')
    duration = request.GET.get('duration')

    if not all([date, time_str, duration]):
        return JsonResponse({'error': 'Необходимы дата, время и продолжительность'}, status=400)

    try:
        # Преобразуем время
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        duration_hours = int(duration)

        # Вычисляем время окончания
        dummy_datetime = datetime.combine(datetime.today(), time_obj)
        end_datetime = dummy_datetime + timedelta(hours=duration_hours)
        end_time = end_datetime.time()

        # Находим занятые столы
        busy_tables = Reservation.objects.filter(
            date=date
        ).exclude(
            Q(end_time__lte=time_obj) | Q(start_time__gte=end_time) | Q(status__in=['cancelled', 'completed'])
        ).values_list('table_id', flat=True)

        # Получаем свободные столы
        free_tables = Table.objects.exclude(
            id__in=busy_tables
        ).filter(
            status=True
        ).values('id', 'number', 'seats', 'hall')

        return JsonResponse(list(free_tables), safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_POST
def reservation_cancel(request, pk):
    reservation = get_object_or_404(Reservation, id=pk)
    if request.user == reservation.user or request.user.is_staff:
        reservation.status = 'cancelled'
        reservation.save()
        return redirect(reverse_lazy("restaurant:reservation_detail", kwargs={'pk': pk}))
    return HttpResponseForbidden("У вас нет прав для отмены этой брони")


@require_POST
def reservation_confirm(request, pk):
    reservation = get_object_or_404(Reservation, id=pk)
    if request.user.is_staff:
        reservation.status = 'active'
        reservation.save()
        return redirect(reverse_lazy("restaurant:reservation_detail", kwargs={'pk': pk}))
    return HttpResponseForbidden("У вас нет прав для подтверждения этой брони")