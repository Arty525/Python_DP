from django.conf.urls.static import static
from django.urls import path

from config import settings
from restaurant import views, services
from restaurant.views import HomePageCreateView, AboutPageTemplateView, ReservationPageCreateView, \
    ReservationDetailView, ReservationUpdateView, ReservationListView, CarouselContentCreateView, \
    ContentManagementTemplateView, DescriptionCreateView, ContactsCreateView, TeamCreateView, HistoryCreateView, \
    MissionCreateView, ServiceCreateView, FeedbackListView, ChiefCreateView, SousChefCreateView

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
    path('content/carousel/create', CarouselContentCreateView.as_view(), name='carousel_create'),
    path('content/restaurant_description/create', DescriptionCreateView.as_view(), name='description_create'),
    path('content/restaurant_history/create', HistoryCreateView.as_view(), name='history_create'),
    path('content/restaurant_mission/create', MissionCreateView.as_view(), name='mission_create'),
    path('contacts/create', ContactsCreateView.as_view(), name='contacts_create'),
    path('service/create', ServiceCreateView.as_view(), name='service_create'),
    path('about/team/create/', TeamCreateView.as_view(), name='team_create'),
    path('about/chief/create/', ChiefCreateView.as_view(), name='chief_create'),
    path('about/sous_chef/create/', SousChefCreateView.as_view(), name='sous_chef_create'),
    path('content/management/', ContentManagementTemplateView.as_view(), name='content_management'),
    path('feedback/list/', FeedbackListView.as_view(), name='feedback_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
