from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("booking/new/", views.booking_create, name="booking_create"),
    path("booking/my/", views.my_bookings, name="my_bookings"),
]
