from django.conf.urls.static import static
from django.urls import path

from config import settings
from restaurant import views
from restaurant.views import HomePageTemplateView, AboutPageTemplateView, ReservationPageCreateView, \
    ReservationDetailView, ReservationUpdateView, ReservationCancelView, ReservationListView

app_name = "restaurant"

urlpatterns = [
    path("", HomePageTemplateView.as_view(), name="home_page"),
    path("about/", AboutPageTemplateView.as_view(), name="about_page"),
    path("new_reservation/", ReservationPageCreateView.as_view(), name="reservation_page"),
    path("reservation/<int:pk>", ReservationDetailView.as_view(), name="reservation_detail"),
    path("reservation/<int:pk>/update/", ReservationUpdateView.as_view(), name="reservation_update"),
    path("reservation/<int:pk>/delete/", ReservationUpdateView.as_view(), name="reservation_delete"),
    path("reservation/<int:pk>/cancel/", ReservationCancelView.as_view(), name="reservation_cancel"),
    path("reservations/list/", ReservationListView.as_view(), name="reservations_list"),
    path('get-free-tables/', views.get_free_tables, name='get_free_tables'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
