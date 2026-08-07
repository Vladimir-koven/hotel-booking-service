from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utils.cache import CacheService
from utils.logger import logger

from .controllers import RoomController
from .serializers import RoomCreateSerializer, RoomSerializer

controller = RoomController()


@api_view(["POST"])
def create_room(request):
    """Создание номера"""
    logger.info(f"POST /rooms/create - Данные: {request.data}")

    serializer = RoomCreateSerializer(data=request.data)
    if not serializer.is_valid():
        logger.warning(f"Ошибка валидации: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        room = controller.create_room(serializer.validated_data)
        # Очищаем кэш после создания
        CacheService.invalidate_pattern("rooms_list")
        logger.success(f"Номер успешно создан: {room.id}")
        return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Ошибка создания номера: {e}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_room(request, room_id):
    """Удаление номера"""
    logger.info(f"DELETE /rooms/delete/{room_id}")

    try:
        controller.delete_room(room_id)
        # Очищаем кэш после удаления
        CacheService.invalidate_pattern("rooms_list")
        logger.success(f"Номер {room_id} удален")
        return Response({"message": "Room deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Ошибка удаления номера {room_id}: {e}")
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def list_rooms(request):
    """Список номеров с кэшированием"""
    filters = {
        "sort_by": request.GET.get("sort_by", "created_at"),
        "order": request.GET.get("order", "desc"),
    }
    logger.info(f"GET /rooms/list - Параметры: {filters}")

    # Создаем ключ кэша на основе фильтров
    cache_key = f"rooms_list_{filters['sort_by']}_{filters['order']}"

    def get_rooms_data():
        rooms = controller.get_rooms_list(filters)
        serializer = RoomSerializer(rooms, many=True)
        return serializer.data

    # Получаем данные из кэша или из БД
    data = CacheService.get_or_set(cache_key, get_rooms_data, timeout=300)
    logger.info(f"Возвращено {len(data)} номеров")
    return Response(data, status=status.HTTP_200_OK)
