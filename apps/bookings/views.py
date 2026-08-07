from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .controllers import BookingController
from .serializers import BookingCreateSerializer, BookingSerializer

controller = BookingController()


@api_view(["POST"])
def create_booking(request):
    serializer = BookingCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        booking = controller.create_booking(serializer.validated_data)
        return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_booking(request, booking_id):
    try:
        controller.delete_booking(booking_id)
        return Response({"message": "Booking deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def list_bookings(request):
    room_id = request.GET.get("room_id")
    if not room_id:
        return Response({"error": "room_id required"}, status=status.HTTP_400_BAD_REQUEST)

    bookings = controller.get_bookings_list(room_id)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
