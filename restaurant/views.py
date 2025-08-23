from django.views import generic
from django.views.generic import TemplateView, CreateView, ListView
from rest_framework.permissions import IsAuthenticated

from restaurant.models import Reservation, Table


class HomePageTemplateView(TemplateView):
    template_name = 'html/index.html'


class AboutPageTemplateView(TemplateView):
    template_name = 'html/about.html'


class ReservationPageTemplateView(CreateView):
    model = Reservation
    template_name = 'html/reservation_page.html'
    fields = '__all__'
    permission_classes = (IsAuthenticated,)


class FreeTablesTemplateView(ListView):
    template_name = 'html/free_tables.html'
    model = Table
    permission_classes = (IsAuthenticated,)
    context_object_name = 'tables'

