from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "date_start", "date_end", "created_at")
    list_filter = ("room", "date_start")
    search_fields = ("room__description",)
