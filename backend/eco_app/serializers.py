from rest_framework import serializers

from .models import EcoBranch
from address_app.serializers import AddressSerializer, LocationSerializer


class EcoBranchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    address = AddressSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = EcoBranch
        fields = ['id', 'name', 'address', 'location', 'working_days', 'information']
