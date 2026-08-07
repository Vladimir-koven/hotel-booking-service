from django.db import models


class Room(models.Model):
    id: models.AutoField = models.AutoField(primary_key=True)
    description: models.TextField = models.TextField(verbose_name="Описание номера")
    price_per_night: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за ночь"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    is_active: models.BooleanField = models.BooleanField(default=True)

    class Meta:
        db_table = "rooms"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Room #{self.id}"

    def soft_delete(self) -> None:
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])
