import ozon3 as ooo
import requests
import pandas as pd
import json

o3 = ooo.Ozon3('3877cc8955afcd70e82ad4942dfb071c86801c7b')

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "latitude": response.get("latitude"),
        "longitude": response.get("longitude")
    }
    return location_data
information = get_location()
latitude = information['latitude']
longitude = information['longitude']
final = o3.get_coordinate_air(latitude, longitude)
#save final to json
#convert final from dataframe to json

#save final to json