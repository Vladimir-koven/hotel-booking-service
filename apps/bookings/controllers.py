from django.core.exceptions import ValidationError
from django.db import transaction

from apps.rooms.models import Room

from .models import Booking


class BookingController:
    @staticmethod
    def create_booking(data):
        try:
            room = Room.objects.get(id=data.get("room_id"), is_active=True)
        except Room.DoesNotExist as e:
            raise ValidationError("Номер не найден") from e

        date_start = data.get("date_start")
        date_end = data.get("date_end")

        overlapping = Booking.objects.filter(
            room=room, date_start__lt=date_end, date_end__gt=date_start
        )
        if overlapping.exists():
            raise ValidationError("Номер уже забронирован на выбранные даты")

        try:
            with transaction.atomic():
                booking = Booking.objects.create(
                    room=room, date_start=date_start, date_end=date_end
                )
                return booking
        except Exception as e:
            raise ValidationError(f"Ошибка создания брони: {e}") from e

    @staticmethod
    def delete_booking(booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.delete()
            return True
        except Booking.DoesNotExist as e:
            raise ValidationError("Бронь не найдена") from e

    @staticmethod
    def get_bookings_list(room_id):
        try:
            room = Room.objects.get(id=room_id, is_active=True)
        except Room.DoesNotExist as e:
            raise ValidationError("Номер не найден") from e
        return Booking.objects.filter(room=room).order_by("date_start")
