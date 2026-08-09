from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.bookings.models import Booking
from apps.rooms.models import Room


class BookingsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_authenticate(user=self.user)
        self.room = Room.objects.create(description="Test Room", price_per_night=100.00)
        self.booking = Booking.objects.create(
            room=self.room,
            date_start=date.today() + timedelta(days=1),
            date_end=date.today() + timedelta(days=5),
        )

    def test_create_booking(self):
        """Создание брони"""
        url = reverse("create_booking")
        data = {
            "room_id": self.room.id,
            "date_start": (date.today() + timedelta(days=10)).isoformat(),
            "date_end": (date.today() + timedelta(days=15)).isoformat(),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("booking_id", response.data)
        self.assertEqual(Booking.objects.count(), 2)

    def test_create_booking_invalid_dates(self):
        """Создание брони с некорректными датами"""
        url = reverse("create_booking")
        data = {"room_id": self.room.id, "date_start": "2024-08-10", "date_end": "2024-08-05"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date_start", response.data)

    def test_create_booking_past_date(self):
        """Создание брони с датой в прошлом"""
        url = reverse("create_booking")
        data = {"room_id": self.room.id, "date_start": "2020-01-01", "date_end": "2020-01-05"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date_start", response.data)

    def test_create_booking_conflict(self):
        """Создание брони с пересечением дат"""
        url = reverse("create_booking")
        data = {
            "room_id": self.room.id,
            "date_start": (self.booking.date_start + timedelta(days=1)).isoformat(),
            "date_end": (self.booking.date_end - timedelta(days=1)).isoformat(),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Номер уже забронирован", str(response.data))

    def test_create_booking_room_not_found(self):
        """Создание брони для несуществующего номера"""
        url = reverse("create_booking")
        data = {
            "room_id": 999,
            "date_start": (date.today() + timedelta(days=1)).isoformat(),
            "date_end": (date.today() + timedelta(days=5)).isoformat(),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_delete_booking(self):
        """Удаление брони"""
        url = reverse("delete_booking", args=[self.booking.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Booking.objects.count(), 0)

    def test_delete_booking_not_found(self):
        """Удаление несуществующей брони"""
        url = reverse("delete_booking", args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_list_bookings(self):
        """Список броней"""
        url = reverse("list_bookings")
        response = self.client.get(url, {"room_id": self.room.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_bookings_no_room_id(self):
        """Список броней без room_id"""
        url = reverse("list_bookings")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_list_bookings_room_not_found(self):
        """Список броней для несуществующего номера"""
        url = reverse("list_bookings")
        response = self.client.get(url, {"room_id": 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_booking_order_by_date(self):
        """Сортировка броней по дате"""
        Booking.objects.create(
            room=self.room,
            date_start=date.today() + timedelta(days=10),
            date_end=date.today() + timedelta(days=15),
        )
        url = reverse("list_bookings")
        response = self.client.get(url, {"room_id": self.room.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Проверка сортировки по date_start
        self.assertTrue(response.data[0]["date_start"] < response.data[1]["date_start"])
