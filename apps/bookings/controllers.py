from django.core.exceptions import ValidationError
from django.db import transaction

from apps.rooms.models import Room
from utils.logger import logger

from .models import Booking


class BookingController:
    """Контроллер для управления бронями"""

    @staticmethod
    def create_booking(data):
        """Создание брони"""
        logger.info(f"Создание брони с данными: {data}")

        try:
            room = Room.objects.get(id=data.get("room_id"), is_active=True)
        except Room.DoesNotExist as e:
            logger.warning(f"Номер {data.get('room_id')} не найден")
            raise ValidationError("Номер не найден") from e

        date_start = data.get("date_start")
        date_end = data.get("date_end")
        logger.debug(f"Проверка доступности номера {room.id} на даты {date_start}-{date_end}")

        # Проверка пересечений
        overlapping = Booking.objects.filter(
            room=room, date_start__lt=date_end, date_end__gt=date_start
        )
        if overlapping.exists():
            logger.warning(f"Конфликт дат для номера {room.id}")
            raise ValidationError("Номер уже забронирован на выбранные даты")

        try:
            with transaction.atomic():
                booking = Booking.objects.create(
                    room=room, date_start=date_start, date_end=date_end
                )
                logger.success(f"Бронь создана, ID: {booking.id}")
                return booking
        except Exception as e:
            logger.error(f"Ошибка создания брони: {e}")
            raise ValidationError(f"Ошибка создания брони: {e}") from e

    @staticmethod
    def delete_booking(booking_id):
        """Удаление брони"""
        logger.info(f"Удаление брони ID: {booking_id}")

        try:
            booking = Booking.objects.get(id=booking_id)
            booking.delete()
            logger.success(f"Бронь {booking_id} удалена")
            return True
        except Booking.DoesNotExist as e:
            logger.warning(f"Бронь {booking_id} не найдена")
            raise ValidationError("Бронь не найдена") from e
        except Exception as e:
            logger.error(f"Ошибка удаления брони {booking_id}: {e}")
            raise

    @staticmethod
    def get_bookings_list(room_id):
        """Получение списка броней"""
        logger.info(f"Получение списка броней для номера {room_id}")

        try:
            room = Room.objects.get(id=room_id, is_active=True)
        except Room.DoesNotExist as e:
            logger.warning(f"Номер {room_id} не найден")
            raise ValidationError("Номер не найден") from e

        bookings = Booking.objects.filter(room=room).order_by("date_start")
        logger.info(f"Найдено {bookings.count()} броней для номера {room_id}")
        return bookings
