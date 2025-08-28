from django.conf.urls.static import static
from django.urls import path

from config import settings
from users.views import ProfileView, CreateUserAPIView, DeleteUserAPIView, UpdateUserAPIView, LoginUserView, \
    UserReservationView, CustomLogoutView, VerifyEmailView, SuccessVerifyView, PasswordRecoveryRequestView, \
    PassRecoveryRequsetSuccess, PasswordChangeView, ChangeUserStatus

app_name = 'users'

urlpatterns = [
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('register/', CreateUserAPIView.as_view(), name='register'),
    path('delete/', DeleteUserAPIView.as_view(), name='delete'),
    path('update/', UpdateUserAPIView.as_view(), name='update'),
    path('login/', LoginUserView.as_view(), name='login'),
    path("logout/", CustomLogoutView.as_view(next_page="sender:index"), name="logout"),
    path('reservation/<int:pk>', UserReservationView.as_view(), name='reservation_detail'),
    path("verify_email/<int:pk>/", VerifyEmailView.as_view(), name="verify_email"),
    path("success_verify/", SuccessVerifyView.as_view(), name="success_verify"),
    path(
        "password_recovery_request/",
        PasswordRecoveryRequestView.as_view(),
        name="password_recovery_request",
    ),
    path(
        "password_recovery_request_success/",
        PassRecoveryRequsetSuccess.as_view(),
        name="password_recovery_request_success",
    ),
    path(
        "password_change/<int:pk>/",
        PasswordChangeView.as_view(),
        name="password_change",
    ),
    path("ban_user/<int:pk>", ChangeUserStatus.as_view(), name="ban_user"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)