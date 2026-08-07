from django.urls import path

from .views import create_room, delete_room, list_rooms

urlpatterns = [
    path("rooms/create", create_room, name="create_room"),
    path("rooms/delete/<int:room_id>", delete_room, name="delete_room"),
    path("rooms/list", list_rooms, name="list_rooms"),
]
