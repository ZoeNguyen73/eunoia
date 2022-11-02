from rest_framework import serializers

from .models import Timeslot

class TimeslotSerializer(serializers.ModelSerializer):
  class Meta:
    model = Timeslot
    fields = [
      'id',
      'listing',
      'date',
      'timeslot_option'
    ]