from django.urls import path
from .views import register_user, login_user, logout_user, MyTokenObtainPairView, user_detail

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name="logout_user"),
    path("detail/", user_detail, name="user_detail"),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
