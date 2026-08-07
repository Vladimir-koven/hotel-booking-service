from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.bookings.models import Booking
from apps.rooms.models import Room


class RoomModelTest(TestCase):
    """Тесты модели Room"""

    def test_create_room(self):
        """Создание номера"""
        room = Room.objects.create(description="Test Room", price_per_night=100.00)
        self.assertEqual(room.description, "Test Room")
        self.assertEqual(room.price_per_night, 100.00)
        self.assertTrue(room.is_active)

    def test_soft_delete(self):
        """Мягкое удаление"""
        room = Room.objects.create(description="Test Room", price_per_night=100.00)
        room.soft_delete()
        self.assertFalse(room.is_active)

    def test_str_method(self):
        """Строковое представление"""
        room = Room.objects.create(description="Test Room", price_per_night=100.00)
        self.assertIn(str(room.id), str(room))


class BookingModelTest(TestCase):
    """Тесты модели Booking"""

    def setUp(self):
        self.room = Room.objects.create(description="Test Room", price_per_night=100.00)

    def test_create_booking(self):
        """Создание брони"""
        booking = Booking.objects.create(
            room=self.room,
            date_start=date.today() + timedelta(days=1),
            date_end=date.today() + timedelta(days=5),
        )
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.date_start, date.today() + timedelta(days=1))
        self.assertEqual(booking.date_end, date.today() + timedelta(days=5))

    def test_invalid_dates(self):
        """Невалидные даты"""
        booking = Booking(
            room=self.room,
            date_start=date.today() + timedelta(days=5),
            date_end=date.today() + timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_str_method(self):
        """Строковое представление"""
        booking = Booking.objects.create(
            room=self.room,
            date_start=date.today() + timedelta(days=1),
            date_end=date.today() + timedelta(days=5),
        )
        self.assertIn(str(booking.id), str(booking))
