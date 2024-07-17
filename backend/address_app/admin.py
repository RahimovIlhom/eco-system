from django.contrib import admin

from .models import Address, Location


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('state', 'city', 'county', 'residential', 'road', 'house_number')
    list_filter = ('state', 'city')
    search_fields = ('state', 'city', 'county', 'residential', 'road', 'house_number')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude')
