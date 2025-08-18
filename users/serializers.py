from rest_framework import serializers
from restaurant.serializers import ReservationSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    payment_history = serializers.SerializerMethodField()

    def get_reservations(self, instance):
        reservations = instance.reservations_set.all()
        return ReservationSerializer(reservations, many=True).data

    class Meta:
        model = User
        fields = "__all__"