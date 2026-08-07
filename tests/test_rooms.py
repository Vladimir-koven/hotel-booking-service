from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.rooms.models import Room


class RoomsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.room = Room.objects.create(description="Test Room", price_per_night=100.00)

    def test_create_room(self):
        url = reverse("create_room")
        data = {"description": "Luxury Suite", "price_per_night": "299.99"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("room_id", response.data)

    def test_list_rooms(self):
        url = reverse("list_rooms")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_delete_room(self):
        url = reverse("delete_room", args=[self.room.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.room.refresh_from_db()
        self.assertFalse(self.room.is_active)
