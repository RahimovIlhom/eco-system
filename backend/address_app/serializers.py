from rest_framework import serializers

from .models import Address, Location


class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'country_uz', 'country_ru', 'state_uz', 'state_ru', 'city_uz', 'city_ru', 'county_uz', 'county_ru', 'residential_uz', 'residential_ru',
                  'neighbourhood_uz', 'neighbourhood_ru', 'road_uz', 'road_ru', 'house_number_uz', 'house_number_ru',
                  'amenity_uz', 'amenity_ru', 'shop_uz', 'shop_ru', 'man_made_uz', 'man_made_ru', 'postcode_uz', 'postcode_ru']


class LocationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Location
        fields = '__all__'
