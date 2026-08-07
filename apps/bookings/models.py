from django.core.exceptions import ValidationError
from django.db import models

from apps.rooms.models import Room


class Booking(models.Model):
    id: models.AutoField = models.AutoField(primary_key=True)
    room: models.ForeignKey = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="bookings", verbose_name="Номер отеля"
    )
    date_start: models.DateField = models.DateField(verbose_name="Дата начала")
    date_end: models.DateField = models.DateField(verbose_name="Дата окончания")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookings"
        ordering = ["date_start"]

    def __str__(self) -> str:
        return f"Booking #{self.id}"

    def clean(self) -> None:
        if self.date_start >= self.date_end:
            raise ValidationError({"date_end": "Дата окончания должна быть позже даты начала"})

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
