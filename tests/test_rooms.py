from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.rooms.models import Room


class RoomsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_authenticate(user=self.user)
        self.room = Room.objects.create(description="Test Room", price_per_night=100.00)
        self.room_data = {"description": "Luxury Suite", "price_per_night": "299.99"}

    def test_create_room(self):
        """Создание номера"""
        url = reverse("create_room")
        response = self.client.post(url, self.room_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("room_id", response.data)
        self.assertEqual(Room.objects.count(), 2)

    def test_create_room_invalid_price(self):
        """Создание номера с невалидной ценой"""
        url = reverse("create_room")
        data = {"description": "Test", "price_per_night": "0"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price_per_night", response.data)

    def test_create_room_negative_price(self):
        """Создание номера с отрицательной ценой"""
        url = reverse("create_room")
        data = {"description": "Test", "price_per_night": "-100"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price_per_night", response.data)

    def test_delete_room(self):
        """Удаление номера"""
        url = reverse("delete_room", args=[self.room.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.room.refresh_from_db()
        self.assertFalse(self.room.is_active)

    def test_delete_room_not_found(self):
        """Удаление несуществующего номера"""
        url = reverse("delete_room", args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_list_rooms(self):
        """Список номеров"""
        url = reverse("list_rooms")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_rooms_sorted_by_price(self):
        """Сортировка по цене"""
        Room.objects.create(description="Room 2", price_per_night=200.00)
        url = reverse("list_rooms")
        response = self.client.get(url, {"sort_by": "price_per_night", "order": "asc"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(float(response.data[0]["price_per_night"]), 100.00)

    def test_list_rooms_sorted_by_date(self):
        """Сортировка по дате"""
        Room.objects.create(description="Room 2", price_per_night=200.00)
        url = reverse("list_rooms")
        response = self.client.get(url, {"sort_by": "created_at", "order": "desc"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_rooms_only_active(self):
        """Только активные номера"""
        Room.objects.create(description="Active Room", price_per_night=150.00)
        self.room.is_active = False
        self.room.save()
        url = reverse("list_rooms")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
