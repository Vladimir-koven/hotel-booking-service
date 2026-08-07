from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utils.logger import logger

from .controllers import BookingController
from .serializers import BookingCreateSerializer, BookingSerializer

controller = BookingController()


@api_view(["POST"])
def create_booking(request):
    """Создание брони"""
    logger.info(f"POST /bookings/create - Данные: {request.data}")

    serializer = BookingCreateSerializer(data=request.data)
    if not serializer.is_valid():
        logger.warning(f"Ошибка валидации: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        booking = controller.create_booking(serializer.validated_data)
        logger.success(f"Бронь успешно создана: {booking.id}")
        return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Ошибка создания брони: {e}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_booking(request, booking_id):
    """Удаление брони"""
    logger.info(f"DELETE /bookings/delete/{booking_id}")

    try:
        controller.delete_booking(booking_id)
        logger.success(f"Бронь {booking_id} удалена")
        return Response({"message": "Booking deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Ошибка удаления брони {booking_id}: {e}")
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def list_bookings(request):
    """Список броней"""
    room_id = request.GET.get("room_id")
    if not room_id:
        logger.warning("GET /bookings/list - Отсутствует параметр room_id")
        return Response({"error": "room_id required"}, status=status.HTTP_400_BAD_REQUEST)

    logger.info(f"GET /bookings/list - room_id: {room_id}")

    try:
        bookings = controller.get_bookings_list(room_id)
        serializer = BookingSerializer(bookings, many=True)
        logger.info(f"Возвращено {len(serializer.data)} броней")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Ошибка получения списка броней: {e}")
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
