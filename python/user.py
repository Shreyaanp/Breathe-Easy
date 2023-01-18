import ozon3 as ooo
import requests
import pandas as pd
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
import json


cred = credentials.Certificate("python\tinyhack-14051-firebase-adminsdk-do0b0-e048e4eaaa.json")
firebase_admin.initialize_app(cred)

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

print("AQI-",int(final.values[0][7]))
##################################################################################################################3

aqival = int(final.values[0][7])
status = "helo"
if(aqival>150):
    status = "WARNING: AQI level is high and may be harmful for asthma affected individuals."

if(aqival<150):
    if(aqival>100):
        status = "WARNING: Wearing a mask is advised"

if(aqival<100):
    status = "GREEN LIGHT: You stay at a place with healty AQI."

final.to_json('file.json', orient = 'split', compression = 'infer', index = 'true')

print(status)
final['suggestion']= [status]
final.to_json('file2.json', orient = 'split', compression = 'infer', index = 'true')

#save json to firebase



ref = db.reference("/users")
with open("file2.json", "r") as f:
	file_contents = json.load(f)
ref.set(file_contents)