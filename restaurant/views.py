from datetime import datetime, timedelta

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
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
    ContactForm, TeamForm, RestaurantHistoryForm, RestaurantMissionForm, ServiceForm, FeedbackForm, ChiefForm, \
    SousChefForm
from restaurant.models import Reservation, Table, Content, Contacts, Team, Service, Feedback, SousChef, Chief
from users.permissions import IsCurrentUser, IsStaff


class HomePageCreateView(CreateView):
    template_name = 'html/index.html'
    form_class = FeedbackForm

    def get_success_url(self):
        return reverse_lazy('restaurant:home_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['slides'] = Content.objects.filter(content_type='carousel', is_active=True)
        except ObjectDoesNotExist:
            context['slides'] = None
        try:
            context['restaurant_description'] = Content.objects.get(content_type='description', is_active=True)
        except ObjectDoesNotExist:
            context['restaurant_description'] = None
        try:
            context['services'] = Service.objects.filter(is_active=True)
        except ObjectDoesNotExist:
            context['services'] = None
        try:
            context['contacts'] = Contacts.objects.latest('id')
        except ObjectDoesNotExist:
            context['contacts'] = None
        return context


class FeedbackListView(ListView):
    model = Feedback
    template_name = 'html/feedback_list.html'
    context_object_name = 'feedback_list'


class FeedbackDetailView(DetailView):
    model = Feedback
    template_name = 'html/feedback_detail.html'
    context_object_name = 'feedback'


class FeedbackDeleteView(DeleteView):
    model = Feedback
    template_name = 'html/feedback_delete.html'
    context_object_name = 'feedback'
    success_url = reverse_lazy('restaurant:home_page')


class AboutPageTemplateView(TemplateView):
    template_name = 'html/about.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['chief'] = Chief.objects.latest('id')
        except ObjectDoesNotExist:
            context['chief'] = None
        try:
            context['sous_chef'] = SousChef.objects.latest('id')
        except ObjectDoesNotExist:
            context['sous_chef'] = None
        try:
            context['team'] = Team.objects.latest('id')
        except ObjectDoesNotExist:
            context['team'] = None
        try:
            context['history'] = Content.objects.filter(content_type='history', is_active=True).latest('id')
        except ObjectDoesNotExist:
            context['history'] = None
        try:
            context['mission'] = Content.objects.filter(content_type='mission', is_active=True).latest('id')
        except ObjectDoesNotExist:
            context['mission'] = None
        return context


class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    template_name = 'html/service_form.html'
    form_class = ServiceForm

    def get_success_url(self):
        return reverse_lazy('restaurant:home_page')


class ServiceListView(ListView):
    model = Service
    template_name = 'html/service_list.html'
    context_object_name = 'services'
    permission_classes = (IsAuthenticated, IsStaff,)


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'html/service_detail.html'
    context_object_name = 'service'
    def post(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        if request.user.is_staff or request.user.is_superuser:
            service.is_active = not service.is_active
            service.save()
            return redirect('restaurant:service_detail', pk=pk)
        return HttpResponseForbidden('У вас нет прав для изменения этой услуги')

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    template_name = 'html/service_form.html'
    form_class = ServiceForm
    def get_success_url(self):
        return reverse_lazy('restaurant:home_page')


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'html/service_delete.html'
    success_url = reverse_lazy('restaurant:home_page')
    def get_success_url(self):
        return reverse_lazy('restaurant:home_page')


class HistoryCreateView(LoginRequiredMixin, CreateView):
    model = Content
    template_name = 'html/history_form.html'
    form_class = RestaurantHistoryForm

    def get_success_url(self):
        return reverse_lazy('restaurant:home_page')


class HistoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Content
    template_name = 'html/history_delete.html'

    def get_success_url(self):
        return reverse_lazy('restaurant:about_page')


class HistoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Content
    template_name = 'html/history_form.html'
    form_class = RestaurantHistoryForm
    def get_success_url(self):
        return reverse_lazy('restaurant:about_page')


class MissionCreateView(LoginRequiredMixin, CreateView):
    model = Content
    template_name = 'html/mission_form.html'
    form_class = RestaurantMissionForm

    def get_success_url(self):
        return reverse_lazy('restaurant:home_page')


class MissionDeleteView(LoginRequiredMixin, DeleteView):
    model = Content
    template_name = 'html/mission_delete.html'
    def get_success_url(self):
        return reverse_lazy('restaurant:about_page')


class MissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Content
    template_name = 'html/mission_form.html'
    form_class = RestaurantMissionForm
    def get_success_url(self):
        return reverse_lazy('restaurant:about_page')


class TeamCreateView(CreateView):
    model = Team
    template_name = 'html/team_form.html'
    form_class = TeamForm

    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = 'html/team_delete.html'
    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    template_name = 'html/team_form.html'
    form_class = TeamForm
    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class ChiefCreateView(CreateView):
    model = Chief
    template_name = 'html/chief_form.html'
    form_class = ChiefForm

    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class ChiefDeleteView(LoginRequiredMixin, DeleteView):
    model = Chief
    template_name = 'html/chief_delete.html'
    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class ChiefUpdateView(LoginRequiredMixin, UpdateView):
    model = Chief
    template_name = 'html/chief_form.html'
    form_class = ChiefForm
    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class SousChefCreateView(CreateView):
    model = SousChef
    template_name = 'html/sous_chef_form.html'
    form_class = SousChefForm

    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class SousChefDeleteView(LoginRequiredMixin, DeleteView):
    model = SousChef
    template_name = 'html/sous_chef_delete.html'
    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class SousChefUpdateView(LoginRequiredMixin, UpdateView):
    model = SousChef
    template_name = 'html/sous_chef_form.html'
    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


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


class CarouselContentCreateView(LoginRequiredMixin, CreateView):
    model = Content
    template_name = 'html/carousel_form.html'
    form_class = CarouselUploadForm
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class CarouselContentUpdateView(LoginRequiredMixin, UpdateView):
    model = Content
    form_class = CarouselUploadForm
    template_name = 'html/carousel_form.html'
    login_url = reverse_lazy("users:login")
    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class CarouselContentDeleteView(LoginRequiredMixin, DeleteView):
    model = Content
    template_name = 'html/carousel_delete.html'
    login_url = reverse_lazy("users:login")
    context_object_name = 'slide'
    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class CarouselContentListView(LoginRequiredMixin, ListView):
    model = Content
    template_name = 'html/carousel_list.html'
    login_url = reverse_lazy("users:login")
    context_object_name = 'slides'

    def get_queryset(self, **kwargs):
        queryset = Content.objects.filter(content_type='carousel')
        print(queryset)
        return queryset

    def post(self, request, pk, *args, **kwargs):
        slide = get_object_or_404(Content, pk=pk)
        if request.user.is_staff or request.user.is_superuser:
            slide.is_active = not slide.is_active
            slide.save()
            return redirect('restaurant:carousel_list')
        return HttpResponseForbidden('У вас нет прав для изменения этого слайда')


class DescriptionCreateView(LoginRequiredMixin, CreateView):
    model = Content
    template_name = 'html/description_form.html'
    form_class = RestaurantDescriptionForm
    login_url = reverse_lazy("users:login")
    permission_classes = (IsAuthenticated, IsStaff,)
    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class DescriptionUpdateView(LoginRequiredMixin, UpdateView):
    model = Content
    form_class = RestaurantDescriptionForm
    login_url = reverse_lazy("users:login")
    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class DescriptionDeleteView(LoginRequiredMixin, DeleteView):
    model = Content
    template_name = 'html/description_form.html'
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


class ContactsUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    login_url = reverse_lazy("users:login")
    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class ContactsDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'html/contact_form.html'
    login_url = reverse_lazy("users:login")
    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")
