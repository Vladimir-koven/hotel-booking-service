from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.bookings.models import Booking
from apps.rooms.models import Room


class BookingsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.room = Room.objects.create(description="Test Room", price_per_night=100.00)
        self.booking = Booking.objects.create(
            room=self.room,
            date_start=date.today() + timedelta(days=1),
            date_end=date.today() + timedelta(days=5),
        )

    def test_create_booking(self):
        url = reverse("create_booking")
        data = {
            "room_id": self.room.id,
            "date_start": (date.today() + timedelta(days=10)).isoformat(),
            "date_end": (date.today() + timedelta(days=15)).isoformat(),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("booking_id", response.data)

    def test_list_bookings(self):
        url = reverse("list_bookings")
        response = self.client.get(url, {"room_id": self.room.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_delete_booking(self):
        url = reverse("delete_booking", args=[self.booking.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)
