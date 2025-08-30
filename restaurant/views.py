from django.http import HttpResponseRedirect
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


class ReservationPageTemplateView(generic.CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'html/reservation_page.html'
    permission_classes = (IsAuthenticated,)
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


