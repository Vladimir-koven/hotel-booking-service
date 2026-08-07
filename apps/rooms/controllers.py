from django.core.exceptions import ValidationError
from django.db import transaction

from apps.bookings.models import Booking

from .models import Room


class RoomController:
    @staticmethod
    def create_room(data):
        try:
            with transaction.atomic():
                room = Room.objects.create(
                    description=data.get("description"), price_per_night=data.get("price_per_night")
                )
                return room
        except Exception as e:
            raise ValidationError(f"Ошибка создания номера: {e}") from e

    @staticmethod
    def delete_room(room_id):
        try:
            room = Room.objects.get(id=room_id, is_active=True)
            Booking.objects.filter(room=room).delete()
            room.soft_delete()
            return True
        except Room.DoesNotExist as e:
            raise ValidationError("Номер не найден") from e

    @staticmethod
    def get_rooms_list(filters=None):
        queryset = Room.objects.filter(is_active=True)
        if filters:
            sort_by = filters.get("sort_by", "created_at")
            order = filters.get("order", "desc")
            if sort_by in ["price_per_night", "created_at"]:
                order_prefix = "-" if order == "desc" else ""
                queryset = queryset.order_by(f"{order_prefix}{sort_by}")
        return queryset
