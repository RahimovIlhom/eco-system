from django.db import models


class Address(models.Model):
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    residential = models.CharField(max_length=255)
    neighbourhood = models.CharField(max_length=255)
    road = models.CharField(max_length=255)
    house_number = models.CharField(max_length=255)
    amenity = models.CharField(max_length=255)
    shop = models.CharField(max_length=255)
    man_made = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.county}, {self.residential}, {self.house_number}"

    class Meta:
        db_table = 'addresses'


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"

    class Meta:
        db_table = 'locations'
