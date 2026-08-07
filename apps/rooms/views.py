from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .controllers import RoomController
from .serializers import RoomCreateSerializer, RoomSerializer

controller = RoomController()


@api_view(["POST"])
def create_room(request):
    serializer = RoomCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        room = controller.create_room(serializer.validated_data)
        return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_room(request, room_id):
    try:
        controller.delete_room(room_id)
        return Response({"message": "Room deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def list_rooms(request):
    filters = {
        "sort_by": request.GET.get("sort_by"),
        "order": request.GET.get("order"),
    }
    rooms = controller.get_rooms_list(filters)
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
