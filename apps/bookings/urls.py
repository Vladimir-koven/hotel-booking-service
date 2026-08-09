from django.urls import path

from .views import create_booking, delete_booking, list_bookings

urlpatterns = [
    path("bookings/create", create_booking, name="create_booking"),
    path("bookings/delete/<int:booking_id>", delete_booking, name="delete_booking"),
    path("bookings/list", list_bookings, name="list_bookings"),
]
