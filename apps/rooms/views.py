from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from utils.logger import logger

from .controllers import RoomController
from .serializers import RoomCreateSerializer, RoomSerializer

controller = RoomController()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_room(request):
    """Создание номера"""
    logger.info(f"POST /rooms/create - Данные: {request.data}")

    serializer = RoomCreateSerializer(data=request.data)
    if not serializer.is_valid():
        logger.warning(f"Ошибка валидации: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    room = controller.create_room(serializer.validated_data)
    logger.success(f"Номер успешно создан: {room.id}")
    return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_room(request, room_id):
    """Удаление номера"""
    logger.info(f"DELETE /rooms/delete/{room_id}")

    controller.delete_room(room_id)
    logger.success(f"Номер {room_id} удален")
    return Response({"message": "Room deleted"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def list_rooms(request):
    """Список номеров"""
    filters = {
        "sort_by": request.GET.get("sort_by", "created_at"),
        "order": request.GET.get("order", "desc"),
    }
    logger.info(f"GET /rooms/list - Параметры: {filters}")

    rooms = controller.get_rooms_list(filters)
    serializer = RoomSerializer(rooms, many=True)
    logger.info(f"Возвращено {len(serializer.data)} номеров")
    return Response(serializer.data, status=status.HTTP_200_OK)
