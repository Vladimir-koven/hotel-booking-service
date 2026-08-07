from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "price_per_night", "created_at", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("description",)
