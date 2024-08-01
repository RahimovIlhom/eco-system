from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="EcoSystemBot")


async def get_location_details(latitude, longitude):
    location = geolocator.reverse((latitude, longitude), exactly_one=True, language='uz')
    address_line = location.address
    address = location.raw['address']
    data = {
        'country_uz': address.get('country', 'N/A'),
        'state_uz': address.get('state', 'N/A'),
        'city_uz': address.get('city', 'N/A'),
        'county_uz': address.get('county', 'N/A'),
        'residential_uz': address.get('residential', 'N/A'),
        'neighbourhood_uz': address.get('neighbourhood', 'N/A'),
        'road_uz': address.get('road', 'N/A'),
        'house_number_uz': address.get('house_number', 'N/A'),
        'amenity_uz': address.get('amenity', 'N/A'),
        'shop_uz': address.get('shop', 'N/A'),
        'man_made_uz': address.get('man_made', 'N/A'),
        'postcode_uz': address.get('postcode', 'N/A'),
        'address_uz': address_line
    }
    location = geolocator.reverse((latitude, longitude), exactly_one=True, language='ru')
    address_line = location.address
    address = location.raw['address']
    data.update({
        'country_ru': address.get('country', 'N/A'),
        'state_ru': address.get('state', 'N/A'),
        'city_ru': address.get('city', 'N/A'),
        'county_ru': address.get('county', 'N/A'),
        'residential_ru': address.get('residential', 'N/A'),
        'neighbourhood_ru': address.get('neighbourhood', 'N/A'),
        'road_ru': address.get('road', 'N/A'),
        'house_number_ru': address.get('house_number', 'N/A'),
        'amenity_ru': address.get('amenity', 'N/A'),
        'shop_ru': address.get('shop', 'N/A'),
        'man_made_ru': address.get('man_made', 'N/A'),
        'postcode_ru': address.get('postcode', 'N/A'),
        'address_ru': address_line
    })

    return data
