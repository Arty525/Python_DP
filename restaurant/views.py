from datetime import datetime, timedelta

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView, UpdateView
from drf_yasg.openapi import Contact
from rest_framework.permissions import IsAuthenticated

from restaurant.forms import ReservationForm, ReservationSearchForm, CarouselUploadForm, RestaurantDescriptionForm, \
    ContactForm
from restaurant.models import Reservation, Table, Content, Contacts
from users.permissions import IsCurrentUser


#from restaurant.serializers import ReservationSerializer


class HomePageTemplateView(TemplateView):
    template_name = 'html/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slides'] = Content.objects.filter(content_type='carousel', is_active=True)
        context['restaurant_description'] = Content.objects.get(content_type='description', is_active=True)
        context['services'] = Content.objects.filter(content_type='services', is_active=True)
        context['contacts'] = Contacts.objects.all()
        return context


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


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'html/reservation_list.html'
    login_url = reverse_lazy("users:login")
    context_object_name = 'reservations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReservationSearchForm(self.request.GET or None)
        context['tables'] = Table.objects.all()
        return context

    def get_queryset(self):
        request_data = self.request.GET.dict()
        if request_data.get('csrfmiddlewaretoken'):
            del request_data['csrfmiddlewaretoken']
        if request_data.get('date') is not None:
            if len(request_data.get('date')) == 0:
                del request_data['date']
        if request_data.get('first_name') is not None:
            if len(request_data.get('first_name')) == 0:
                del request_data['first_name']
        if request_data.get('last_name') is not None:
            if len(request_data.get('last_name')) == 0:
                del request_data['last_name']
        print(request_data)
        context_data = Reservation.objects.filter(**request_data)
        return context_data


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


class ContentManagementTemplateView(TemplateView):
    template_name = 'html/content_management.html'
    login_url = reverse_lazy("users:login")


class CarouselContentCreateView(LoginRequiredMixin, CreateView):
    model = Content
    template_name = 'html/carousel_form.html'
    form_class = CarouselUploadForm
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class DescriptionCreateView(LoginRequiredMixin, CreateView):
    model = Content
    template_name = 'html/description_form.html'
    form_class = RestaurantDescriptionForm
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class ContactsCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = 'html/contact_form.html'
    form_class = ContactForm
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")

# class ReservationCancelView(LoginRequiredMixin, View):
#     permission_required = (IsAuthenticated,)
#     def post(self, request, pk):
#         reservation = get_object_or_404(Reservation, id=pk)
#         if request.user == reservation.user or request.user.is_staff:
#             reservation.status = 'cancelled'
#             reservation.save()
#             return redirect(reverse_lazy("restaurant:reservation_detail", kwargs={'pk': pk}))
#         return HttpResponseForbidden("У вас нет прав для отключения этой рассылки")



