from rest_framework import serializers

from events.models import Venue


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"
