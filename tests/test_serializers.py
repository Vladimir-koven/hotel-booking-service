from datetime import date, timedelta

from django.test import TestCase

from apps.bookings.models import Booking
from apps.bookings.serializers import BookingCreateSerializer, BookingSerializer
from apps.rooms.models import Room
from apps.rooms.serializers import RoomCreateSerializer, RoomSerializer


class RoomSerializerTest(TestCase):
    """Тесты сериализаторов Room"""

    def test_valid_room_create_serializer(self):
        data = {"description": "Люкс", "price_per_night": "299.99"}
        serializer = RoomCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["description"], "Люкс")

    def test_invalid_room_create_serializer_zero_price(self):
        data = {"description": "Люкс", "price_per_night": "0"}
        serializer = RoomCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("price_per_night", serializer.errors)

    def test_room_serializer(self):
        room = Room.objects.create(description="Тест", price_per_night=150.00)
        serializer = RoomSerializer(room)
        self.assertEqual(serializer.data["id"], room.id)


class BookingSerializerTest(TestCase):
    """Тесты сериализаторов Booking"""

    def setUp(self):
        self.room = Room.objects.create(description="Тест", price_per_night=100.00)

    def test_valid_booking_create_serializer(self):
        data = {
            "room_id": self.room.id,
            "date_start": (date.today() + timedelta(days=1)).isoformat(),
            "date_end": (date.today() + timedelta(days=5)).isoformat(),
        }
        serializer = BookingCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_booking_create_serializer_past_date(self):
        data = {
            "room_id": self.room.id,
            "date_start": (date.today() - timedelta(days=1)).isoformat(),
            "date_end": (date.today() + timedelta(days=5)).isoformat(),
        }
        serializer = BookingCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("date_start", serializer.errors)

    def test_booking_serializer(self):
        booking = Booking.objects.create(
            room=self.room,
            date_start=date.today() + timedelta(days=1),
            date_end=date.today() + timedelta(days=5),
        )
        serializer = BookingSerializer(booking)
        self.assertEqual(serializer.data["id"], booking.id)
