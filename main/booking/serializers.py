from rest_framework import serializers
from .models import Booking, Appliance

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'appliance', 'day_from', 'day_to', 'user']