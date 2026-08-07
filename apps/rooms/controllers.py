from django.core.exceptions import ValidationError
from django.db import transaction

from apps.bookings.models import Booking
from utils.logger import logger

from .models import Room


class RoomController:
    """Контроллер для управления номерами"""

    @staticmethod
    def create_room(data):
        """Создание номера"""
        logger.info(f"Создание номера с данными: {data}")
        try:
            with transaction.atomic():
                room = Room.objects.create(
                    description=data.get("description"), price_per_night=data.get("price_per_night")
                )
                logger.success(f"Номер создан, ID: {room.id}")
                return room
        except Exception as e:
            logger.error(f"Ошибка создания номера: {e}")
            raise ValidationError(f"Ошибка создания номера: {e}") from e

    @staticmethod
    def delete_room(room_id):
        """Удаление номера (мягкое)"""
        logger.info(f"Удаление номера ID: {room_id}")
        try:
            room = Room.objects.get(id=room_id, is_active=True)
            bookings_count = Booking.objects.filter(room=room).count()
            Booking.objects.filter(room=room).delete()
            room.soft_delete()
            logger.success(f"Номер {room_id} удален, удалено броней: {bookings_count}")
            return True
        except Room.DoesNotExist as e:
            logger.warning(f"Номер {room_id} не найден")
            raise ValidationError("Номер не найден") from e
        except Exception as e:
            logger.error(f"Ошибка удаления номера {room_id}: {e}")
            raise

    @staticmethod
    def get_rooms_list(filters=None):
        """Получение списка номеров с фильтрацией"""
        logger.debug(f"Получение списка номеров с фильтрами: {filters}")
        queryset = Room.objects.filter(is_active=True)
        if filters:
            sort_by = filters.get("sort_by", "created_at")
            order = filters.get("order", "desc")
            if sort_by in ["price_per_night", "created_at"]:
                order_prefix = "-" if order == "desc" else ""
                queryset = queryset.order_by(f"{order_prefix}{sort_by}")
                logger.debug(f"Сортировка по {sort_by} ({order})")
        logger.info(f"Найдено {queryset.count()} номеров")
        return queryset
