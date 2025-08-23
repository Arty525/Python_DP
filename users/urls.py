from django.urls import path

from users.views import ProfileView, CreateUserAPIView, DeleteUserAPIView, UpdateUserAPIView, LoginUserView, \
    UserReservationView

app_name = 'users'

urlpatterns = [
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('register/', CreateUserAPIView.as_view(), name='register'),
    path('delete/', DeleteUserAPIView.as_view(), name='delete'),
    path('update/', UpdateUserAPIView.as_view(), name='update'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('reservation/<int:pk>', UserReservationView.as_view(), name='reservation_detail'),
]