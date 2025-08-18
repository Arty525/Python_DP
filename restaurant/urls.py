from django.urls import path

from restaurant.views import HomePageTemplateView, AboutPageTemplateView, ReservationPageTemplateView

app_name = "restaurant"

urlpatterns = [
    path("", HomePageTemplateView.as_view(), name="home_page"),
    path("about/", AboutPageTemplateView.as_view(), name="about_page"),
    path("reservation/", ReservationPageTemplateView.as_view(), name="reservation_page"),
]
