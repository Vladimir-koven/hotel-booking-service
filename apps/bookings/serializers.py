from datetime import date

from rest_framework import serializers

from .models import Booking


class BookingCreateSerializer(serializers.Serializer):
    room_id = serializers.IntegerField(required=True)
    date_start = serializers.DateField(required=True, input_formats=["%Y-%m-%d"])
    date_end = serializers.DateField(required=True, input_formats=["%Y-%m-%d"])

    def validate_date_start(self, value):
        if value < date.today():
            raise serializers.ValidationError("Дата начала не может быть в прошлом")
        return value

    def validate(self, data):
        if data["date_start"] >= data["date_end"]:
            raise serializers.ValidationError("Дата начала должна быть раньше даты окончания")
        return data


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "room_id", "date_start", "date_end", "created_at"]
