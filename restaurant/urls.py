from django.conf.urls.static import static
from django.urls import path

from config import settings
from restaurant.views import HomePageTemplateView, AboutPageTemplateView, ReservationPageTemplateView, \
    FreeTablesTemplateView

app_name = "restaurant"

urlpatterns = [
    path("", HomePageTemplateView.as_view(), name="home_page"),
    path("about/", AboutPageTemplateView.as_view(), name="about_page"),
    path("new_reservation/", ReservationPageTemplateView.as_view(), name="reservation_page"),
    path("free_tables/", FreeTablesTemplateView.as_view(), name="free_tables"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
