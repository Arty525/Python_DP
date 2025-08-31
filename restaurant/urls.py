from django.conf.urls.static import static
from django.urls import path

from config import settings
from restaurant import views
from restaurant.views import HomePageTemplateView, AboutPageTemplateView, ReservationPageCreateView, \
    FreeTablesTemplateView

app_name = "restaurant"

urlpatterns = [
    path("", HomePageTemplateView.as_view(), name="home_page"),
    path("about/", AboutPageTemplateView.as_view(), name="about_page"),
    path("new_reservation/", ReservationPageCreateView.as_view(), name="reservation_page"),
    path("free_tables/", FreeTablesTemplateView.as_view(), name="free_tables"),
    path('get-free-tables/', views.get_free_tables, name='get_free_tables'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
