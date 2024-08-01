from modeltranslation.translator import translator, TranslationOptions
from .models import Address


class AddressTranslationOptions(TranslationOptions):
    fields = ('country', 'state', 'city', 'county', 'residential', 'neighbourhood', 'road', 'house_number', 'amenity', 'shop', 'man_made', 'postcode', 'address')


translator.register(Address, AddressTranslationOptions)
