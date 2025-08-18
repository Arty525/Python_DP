from django.views import generic
from rest_framework.permissions import IsAuthenticated


class HomePageTemplateView(generic.TemplateView):
    template_name = 'html/index.html'


class AboutPageTemplateView(generic.TemplateView):
    template_name = 'html/about.html'


class ReservationPageTemplateView(generic.TemplateView):
    template_name = 'html/reservation.html'
    permission_classes = (IsAuthenticated,)

