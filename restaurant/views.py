from datetime import datetime, timedelta
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView, UpdateView
from restaurant.forms import ReservationForm, ReservationSearchForm, CarouselUploadForm, RestaurantDescriptionForm, \
    ContactForm, TeamForm, RestaurantHistoryForm, RestaurantMissionForm, ServiceForm, FeedbackForm, ChiefForm, \
    SousChefForm
from restaurant.models import Reservation, Table, Content, Contacts, Team, Service, Feedback, SousChef, Chief



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


class FeedbackListView(PermissionRequiredMixin, ListView):
    model = Feedback
    template_name = 'html/feedback_list.html'
    context_object_name = 'feedback_list'
    permission_required = 'restaurant.view_feedback'
    login_url = reverse_lazy("users:login")


class FeedbackDetailView(PermissionRequiredMixin, DetailView):
    model = Feedback
    template_name = 'html/feedback_detail.html'
    context_object_name = 'feedback'
    permission_required = 'restaurant.view_feedback'
    login_url = reverse_lazy("users:login")


class FeedbackUpdateView(PermissionRequiredMixin, UpdateView):
    model = Feedback
    template_name = 'html/feedback_update.html'
    form_class = FeedbackForm
    permission_required = 'restaurant.change_feedback'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy('restaurant:feedback_list')


class FeedbackDeleteView(PermissionRequiredMixin, DeleteView):
    model = Feedback
    template_name = 'html/feedback_delete.html'
    context_object_name = 'feedback'
    success_url = reverse_lazy('restaurant:home_page')
    permission_required = 'restaurant.delete_feedback'
    login_url = reverse_lazy("users:login")


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


class ServiceCreateView(PermissionRequiredMixin, CreateView):
    model = Service
    template_name = 'html/service_form.html'
    form_class = ServiceForm
    permission_required = 'restaurant.add_service'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy('restaurant:home_page')


class ServiceListView(PermissionRequiredMixin, ListView):
    model = Service
    template_name = 'html/service_list.html'
    context_object_name = 'services'
    permission_required = 'restaurant.view_service'
    login_url = reverse_lazy("users:login")


class ServiceDetailView(PermissionRequiredMixin, DetailView):
    model = Service
    template_name = 'html/service_detail.html'
    context_object_name = 'service'
    permission_required = 'restaurant.view_service'
    login_url = reverse_lazy("users:login")

    def post(self, request, pk):
        if not request.user.has_perm('restaurant.change_service'):
            return HttpResponseForbidden('У вас нет прав для изменения этой услуги')

        service = get_object_or_404(Service, pk=pk)
        service.is_active = not service.is_active
        service.save()
        return redirect('restaurant:service_detail', pk=pk)


class ServiceUpdateView(PermissionRequiredMixin, UpdateView):
    model = Service
    template_name = 'html/service_form.html'
    form_class = ServiceForm
    permission_required = 'restaurant.change_service'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy('restaurant:home_page')


class ServiceDeleteView(PermissionRequiredMixin, DeleteView):
    model = Service
    template_name = 'html/service_delete.html'
    success_url = reverse_lazy('restaurant:home_page')
    permission_required = 'restaurant.delete_service'
    login_url = reverse_lazy("users:login")


class HistoryCreateView(PermissionRequiredMixin, CreateView):
    model = Content
    template_name = 'html/history_form.html'
    form_class = RestaurantHistoryForm
    permission_required = 'restaurant.add_content'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy('restaurant:home_page')


class HistoryUpdateView(PermissionRequiredMixin, UpdateView):
    model = Content
    template_name = 'html/history_form.html'
    form_class = RestaurantHistoryForm
    permission_required = 'restaurant.change_content'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy('restaurant:about_page')


class HistoryDeleteView(PermissionRequiredMixin, DeleteView):
    model = Content
    template_name = 'html/history_delete.html'
    context_object_name = 'history'
    permission_required = 'restaurant.delete_content'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy('restaurant:about_page')


class MissionCreateView(PermissionRequiredMixin, CreateView):
    model = Content
    template_name = 'html/mission_form.html'
    form_class = RestaurantMissionForm
    permission_required = 'restaurant.add_content'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy('restaurant:home_page')


class MissionDeleteView(PermissionRequiredMixin, DeleteView):
    model = Content
    template_name = 'html/mission_delete.html'
    context_object_name = 'mission'
    permission_required = 'restaurant.delete_content'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy('restaurant:about_page')


class MissionUpdateView(PermissionRequiredMixin, UpdateView):
    model = Content
    template_name = 'html/mission_form.html'
    form_class = RestaurantMissionForm
    permission_required = 'restaurant.change_content'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy('restaurant:about_page')


class TeamCreateView(PermissionRequiredMixin, CreateView):
    model = Team
    template_name = 'html/team_form.html'
    form_class = TeamForm
    permission_required = 'restaurant.add_team'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class TeamDeleteView(PermissionRequiredMixin, DeleteView):
    model = Team
    template_name = 'html/team_delete.html'
    context_object_name = 'team'
    permission_required = 'restaurant.delete_team'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class TeamUpdateView(PermissionRequiredMixin, UpdateView):
    model = Team
    template_name = 'html/team_form.html'
    form_class = TeamForm
    permission_required = 'restaurant.change_team'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class ChiefCreateView(PermissionRequiredMixin, CreateView):
    model = Chief
    template_name = 'html/chief_form.html'
    form_class = ChiefForm
    permission_required = 'restaurant.add_chief'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class ChiefDeleteView(PermissionRequiredMixin, DeleteView):
    model = Chief
    template_name = 'html/chief_delete.html'
    context_object_name = 'chief'
    permission_required = 'restaurant.delete_chief'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class ChiefUpdateView(PermissionRequiredMixin, UpdateView):
    model = Chief
    template_name = 'html/chief_form.html'
    form_class = ChiefForm
    permission_required = 'restaurant.change_chief'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class SousChefCreateView(PermissionRequiredMixin, CreateView):
    model = SousChef
    template_name = 'html/sous_chef_form.html'
    form_class = SousChefForm
    permission_required = 'restaurant.add_souschef'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class SousChefDeleteView(PermissionRequiredMixin, DeleteView):
    model = SousChef
    template_name = 'html/sous_chef_delete.html'
    context_object_name = 'sous_chef'
    permission_required = 'restaurant.delete_souschef'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class SousChefUpdateView(PermissionRequiredMixin, UpdateView):
    model = SousChef
    form_class = SousChefForm
    template_name = 'html/sous_chef_form.html'
    permission_required = 'restaurant.change_souschef'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:about_page")


class ReservationPageCreateView(PermissionRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'html/reservation_page.html'
    permission_required = 'restaurant.add_reservation'
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


class ReservationListView(PermissionRequiredMixin, ListView):
    model = Reservation
    template_name = 'html/reservation_list.html'
    permission_required = 'restaurant.view_reservation'
    login_url = reverse_lazy("users:login")
    context_object_name = 'reservations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReservationSearchForm(self.request.GET or None)
        context['tables'] = Table.objects.all()
        return context

    def get_queryset(self):
        request_data = self.request.GET.dict()
        print(request_data)
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


class ReservationDetailView(PermissionRequiredMixin, DetailView):
    model = Reservation
    template_name = 'html/reservation_detail.html'
    permission_required = 'restaurant.view_reservation'
    login_url = reverse_lazy("users:login")
    context_object_name = 'reservation'


class ReservationDeleteView(PermissionRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'html/reservation_delete.html'
    permission_required = 'restaurant.delete_reservation'
    login_url = reverse_lazy("users:login")
    context_object_name = 'reservation'

    def get_success_url(self):
        return reverse_lazy("users:profile", kwargs={'pk': self.request.user.pk})


class ReservationUpdateView(PermissionRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'html/reservation_update.html'
    permission_required = 'restaurant.change_reservation'
    login_url = reverse_lazy("users:login")
    context_object_name = 'reservation'

    def get_success_url(self):
        return reverse_lazy("users:profile", kwargs={'pk': self.object.pk})


class CarouselContentCreateView(PermissionRequiredMixin, CreateView):
    model = Content
    template_name = 'html/carousel_form.html'
    form_class = CarouselUploadForm
    permission_required = 'restaurant.add_content'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class CarouselContentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Content
    form_class = CarouselUploadForm
    template_name = 'html/carousel_form.html'
    permission_required = 'restaurant.change_content'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class CarouselContentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Content
    template_name = 'html/carousel_delete.html'
    permission_required = 'restaurant.delete_content'
    login_url = reverse_lazy("users:login")
    context_object_name = 'slide'

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class CarouselContentListView(PermissionRequiredMixin, ListView):
    model = Content
    template_name = 'html/carousel_list.html'
    permission_required = 'restaurant.view_content'
    login_url = reverse_lazy("users:login")
    context_object_name = 'slides'

    def get_queryset(self, **kwargs):
        queryset = Content.objects.filter(content_type='carousel')
        print(queryset)
        return queryset

    def post(self, request, pk, *args, **kwargs):
        if not request.user.has_perm('restaurant.change_content'):
            return HttpResponseForbidden('У вас нет прав для изменения этого слайда')

        slide = get_object_or_404(Content, pk=pk)
        slide.is_active = not slide.is_active
        slide.save()
        return redirect('restaurant:carousel_list')


class DescriptionCreateView(PermissionRequiredMixin, CreateView):
    model = Content
    template_name = 'html/description_form.html'
    form_class = RestaurantDescriptionForm
    permission_required = 'restaurant.add_content'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class DescriptionUpdateView(PermissionRequiredMixin, UpdateView):
    model = Content
    form_class = RestaurantDescriptionForm
    template_name = 'html/description_form.html'
    permission_required = 'restaurant.change_content'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class DescriptionDeleteView(PermissionRequiredMixin, DeleteView):
    model = Content
    template_name = 'html/description_form.html'
    permission_required = 'restaurant.delete_content'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class ContactsCreateView(PermissionRequiredMixin, CreateView):
    model = Contacts
    template_name = 'html/contact_form.html'
    form_class = ContactForm
    permission_required = 'restaurant.add_contacts'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class ContactsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Contacts
    template_name = 'html/contact_form.html'
    form_class = ContactForm
    permission_required = 'restaurant.change_contacts'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")


class ContactsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Contacts
    template_name = 'html/contact_form.html'
    permission_required = 'restaurant.delete_contacts'
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("restaurant:home_page")