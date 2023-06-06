from geopy.geocoders import Nominatim
import brazilcep
from time import sleep


def get_adress(cep: str) -> str:
    print('get_adress')
    try:
        address = brazilcep.get_address_from_cep(cep)
        if address['street'] and address['district']:
            return f"{address['street']}, {address['district']}-{address['city']}"
        sleep(1)
        return address['city']
    except Exception as e:
        print('Exception: ', e)


def get_coordinates(address: str):
    print('get_coordinates')
    print(address)
    geolocator = Nominatim(user_agent='RFB_CNPJ_APP')
    return geolocator.geocode(address)


def from_cep_to_coordinates(pais, estado):
    print('from_cep_to_coordinates')
    query = {
        'country': pais,
        'state': estado,
    }

    coordinates = get_coordinates(query)
    print(coordinates, coordinates.latitude, coordinates.longitude)
    return coordinates.latitude, coordinates.longitude