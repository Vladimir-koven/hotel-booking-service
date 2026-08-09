from rest_framework import serializers

from .models import Room


class RoomCreateSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=1000, required=True)
    price_per_night = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=True, min_value=0.01
    )

    def validate_price_per_night(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше 0")
        return value


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "description", "price_per_night", "created_at"]
