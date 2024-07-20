from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="EcoSystemBot")


async def get_location_details(latitude, longitude):
    location = geolocator.reverse((latitude, longitude), exactly_one=True, language='uz')
    address = location.raw['address']

    return {
        'country': address.get('country', 'N/A'),
        'state': address.get('state', 'N/A'),
        'city': address.get('city', 'N/A'),
        'county': address.get('county', 'N/A'),
        'residential': address.get('residential', 'N/A'),
        'neighbourhood': address.get('neighbourhood', 'N/A'),
        'road': address.get('road', 'N/A'),
        'house_number': address.get('house_number', 'N/A'),
        'amenity': address.get('amenity', 'N/A'),
        'shop': address.get('shop', 'N/A'),
        'man_made': address.get('man_made', 'N/A'),
        'postcode': address.get('postcode', 'N/A'),
    }
