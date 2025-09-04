from django.conf.urls.static import static
from django.urls import path

from config import settings
from restaurant import services
from restaurant.views import (HomePageCreateView, AboutPageTemplateView, ReservationPageCreateView, \
                              ReservationDetailView, ReservationUpdateView, ReservationListView,
                              CarouselContentCreateView,
                              DescriptionCreateView, ContactsCreateView, TeamCreateView, HistoryCreateView, \
                              MissionCreateView, ServiceCreateView, FeedbackListView, ChiefCreateView,
                              SousChefCreateView, ServiceListView, \
                              ServiceDetailView, ServiceDeleteView, ServiceUpdateView, CarouselContentUpdateView,
                              CarouselContentListView, \
                              CarouselContentDeleteView, DescriptionUpdateView, DescriptionDeleteView,
                              HistoryUpdateView, HistoryDeleteView, \
                              MissionDeleteView, MissionUpdateView, ContactsUpdateView, ContactsDeleteView,
                              TeamUpdateView, TeamDeleteView, \
                              ChiefUpdateView, ChiefDeleteView, SousChefUpdateView, SousChefDeleteView,
                              FeedbackDetailView, FeedbackDeleteView, FeedbackUpdateView)

app_name = "restaurant"

urlpatterns = [
    path("", HomePageCreateView.as_view(), name="home_page"),
    path("about/", AboutPageTemplateView.as_view(), name="about_page"),

    path("new_reservation/", ReservationPageCreateView.as_view(), name="reservation_page"),
    path("reservation/<int:pk>", ReservationDetailView.as_view(), name="reservation_detail"),
    path("reservation/<int:pk>/update/", ReservationUpdateView.as_view(), name="reservation_update"),
    path("reservation/<int:pk>/delete/", ReservationUpdateView.as_view(), name="reservation_delete"),
    path("reservation/<int:pk>/cancel/", services.reservation_cancel, name="reservation_cancel"),
    path("reservation/<int:pk>/confirm/", services.reservation_confirm, name="reservation_confirm"),
    path("reservations/list/", ReservationListView.as_view(), name="reservations_list"),
    path('get-free-tables/', services.get_free_tables, name='get_free_tables'),

    path('content/carousel/create/', CarouselContentCreateView.as_view(), name='carousel_create'),
    path('content/carousel/update/<int:pk>', CarouselContentUpdateView.as_view(), name='carousel_update'),
    path('content/carousel/list/', CarouselContentListView.as_view(), name='carousel_list'),
    path('content/carousel/delete/<int:pk>', CarouselContentDeleteView.as_view(), name='carousel_delete'),

    path('content/restaurant_description/create/', DescriptionCreateView.as_view(), name='description_create'),
    path('content/restaurant_description/update/<int:pk>', DescriptionUpdateView.as_view(), name='description_update'),
    path('content/restaurant_description/delete/<int:pk>', DescriptionDeleteView.as_view(), name='description_delete'),

    path('content/restaurant_history/create/', HistoryCreateView.as_view(), name='history_create'),
    path('content/restaurant_history/update/<int:pk>', HistoryUpdateView.as_view(), name='history_update'),
    path('content/restaurant_history/delete/<int:pk>', HistoryDeleteView.as_view(), name='history_delete'),

    path('content/restaurant_mission/create/', MissionCreateView.as_view(), name='mission_create'),
    path('content/restaurant_mission/update/<int:pk>', MissionUpdateView.as_view(), name='mission_update'),
    path('content/restaurant_mission/delete/<int:pk>', MissionDeleteView.as_view(), name='mission_delete'),

    path('contacts/create/', ContactsCreateView.as_view(), name='contacts_create'),
    path('contacts/update/<int:pk>', ContactsUpdateView.as_view(), name='contacts_update'),
    path('contacts/delete/<int:pk>', ContactsDeleteView.as_view(), name='contacts_delete'),

    path('service/create/', ServiceCreateView.as_view(), name='service_create'),
    path('service/list/', ServiceListView.as_view(), name='service_list'),
    path('service/delete/<int:pk>', ServiceDeleteView.as_view(), name='service_delete'),
    path('service/update/<int:pk>', ServiceUpdateView.as_view(), name='service_update'),
    path('service/detail/<int:pk>', ServiceDetailView.as_view(), name='service_detail'),

    path('about/team/create/', TeamCreateView.as_view(), name='team_create'),
    path('about/team/update/<int:pk>', TeamUpdateView.as_view(), name='team_update'),
    path('about/team/delete/<int:pk>', TeamDeleteView.as_view(), name='team_delete'),

    path('about/chief/create/', ChiefCreateView.as_view(), name='chief_create'),
    path('about/chief/update/<int:pk>', ChiefUpdateView.as_view(), name='chief_update'),
    path('about/chief/delete/<int:pk>', ChiefDeleteView.as_view(), name='chief_delete'),

    path('about/sous_chef/create/', SousChefCreateView.as_view(), name='sous_chef_create'),
    path('about/sous_chef/update/<int:pk>', SousChefUpdateView.as_view(), name='sous_chef_update'),
    path('about/sous_chef/delete/<int:pk>', SousChefDeleteView.as_view(), name='sous_chef_delete'),

    path('feedback/list/', FeedbackListView.as_view(), name='feedback_list'),
    path('feedback/detail/<int:pk>', FeedbackDetailView.as_view(), name='feedback_detail'),
    path('feedback/delete/<int:pk>', FeedbackDeleteView.as_view(), name='feedback_delete'),
    path('feedback/update/<int:pk>', FeedbackUpdateView.as_view(), name='feedback_update'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
