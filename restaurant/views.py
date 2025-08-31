from datetime import datetime, timedelta

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, CreateView, ListView
from rest_framework.permissions import IsAuthenticated

from restaurant.forms import ReservationForm
from restaurant.models import Reservation, Table
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

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FreeTablesTemplateView(ListView):
    template_name = 'html/free_tables.html'
    model = Table
    permission_classes = (IsAuthenticated,)
    context_object_name = 'tables'


    def get_queryset(self, **kwargs):
        date = self.request.GET.get('date')
        time = self.request.GET.get('start_time')
        duration = int(self.request.GET.get('duration'))
        dummy_datetime = datetime.combine(datetime.today(), datetime.strptime(time, '%H:%M').time())
        end_time = (dummy_datetime + timedelta(hours=duration)).time()
        print(f"Date: {date}, Time: {time}, Duration: {duration}")  # для отладки
        free_tables = []
        reservations = Reservation.objects.filter(date=date)
        print(reservations)
        for reservation in reservations:
            if reservation.start_time <= time <= reservation.end_time:
                if reservation.start_time <= time <= reservation.end_time:
                    free_tables.append(reservation.table)
        queryset = Table.objects.exclude(number__in=free_tables)
        print(queryset)
        return queryset


