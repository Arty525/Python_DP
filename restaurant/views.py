from datetime import datetime, timedelta

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView, UpdateView
from rest_framework.permissions import IsAuthenticated

from restaurant.forms import ReservationForm
from restaurant.models import Reservation, Table
from users.permissions import IsCurrentUser


#from restaurant.serializers import ReservationSerializer


class HomePageTemplateView(TemplateView):
    template_name = 'html/index.html'


class AboutPageTemplateView(TemplateView):
    template_name = 'html/about.html'


class ReservationPageCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'html/reservation_page.html'
    login_url = reverse_lazy("users:login")
    context_object_name = 'tables'

    def get_queryset(self, **kwargs):
        if self.request.GET.get('date') and self.request.GET.get('start_time') and self.request.GET.get('duration'):
            date = self.request.GET.get('date')
            time = self.request.GET.get('start_time')
            duration = int(self.request.GET.get('duration'))
            dummy_datetime = datetime.combine(datetime.today(), datetime.strptime(time, '%H:%M').time())
            end_time = (dummy_datetime + timedelta(hours=duration)).time()
            free_tables = []
            reservations = Reservation.objects.filter(date=date)
            for reservation in reservations:
                if reservation.start_time <= datetime.strptime(time, '%H:%M').time() <= reservation.end_time:
                    free_tables.append(reservation.table.number)
                if reservation.start_time <= end_time <= reservation.end_time:
                    free_tables.append(reservation.table.number)
            queryset = Table.objects.exclude(number__in=free_tables)
        else:
            queryset = {}
        return queryset

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = 'html/reservation_detail.html'
    login_url = reverse_lazy("users:login")
    context_object_name = 'reservation'


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'html/reservation_delete.html'
    login_url = reverse_lazy("users:login")
    context_object_name = 'reservation'

    def get_success_url(self):
        return reverse_lazy("users:profile", kwargs={'pk': self.request.user.pk})


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'html/reservation_update.html'
    login_url = reverse_lazy("users:login")
    context_object_name = 'reservation'

    def get_success_url(self):
        return reverse_lazy("users:profile", kwargs={'pk': self.object.pk})


class ReservationCancelView(LoginRequiredMixin, View):
    permission_required = (IsAuthenticated,)
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, id=pk)
        if request.user == reservation.user:
            reservation.status = 'cancelled'
            reservation.save()
            return redirect(reverse_lazy("restaurant:reservation_detail", kwargs={'pk': pk}))
        return HttpResponseForbidden("У вас нет прав для отключения этой рассылки")



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
            Q(end_time__lte=time_obj) | Q(start_time__gte=end_time)
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