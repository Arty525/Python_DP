# from rest_framework import serializers
# from .models import Reservation, Table, Content
# from .validators import ReservationDateValidator, ReservationTimeValidator, ReservationGuestsValidator
#
#
# class ReservationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reservation
#         fields = '__all__'
#         validators = [ReservationDateValidator(field="date"),
#                       ReservationTimeValidator(field="time"),
#                       ReservationGuestsValidator(field="guests"), ]
#
#
# class TableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Table
#         fields = '__all__'
#
#
# class ContentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Content
#         fields = '__all__'
