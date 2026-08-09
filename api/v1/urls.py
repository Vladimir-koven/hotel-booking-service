from django.urls import include, path

urlpatterns = [
    path("", include("apps.rooms.urls")),
    path("", include("apps.bookings.urls")),
    path("", include("apps.users.urls")),
]
