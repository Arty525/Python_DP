from django.urls import path

from users.views import RetriveUserAPIView, CreateUserAPIView, DeleteUserAPIView, UpdateUserAPIView, LoginUserView

app_name = 'users'

urlpatterns = [
    path('profile/', RetriveUserAPIView.as_view(), name='profile'),
    path('register/', CreateUserAPIView.as_view(), name='create'),
    path('delete/', DeleteUserAPIView.as_view(), name='delete'),
    path('update/', UpdateUserAPIView.as_view(), name='update'),
    path('login/', LoginUserView.as_view(), name='login'),
]