# import phonenumbers
# from phonenumbers import geocoder
# import folium
# from opencage.geocoder import OpenCageGeocode
# from phonenumbers import carrier

# number = input("Enter the phone number with country code: ")
# check_number = phonenumbers.parse(number)
# number_location = geocoder.description_for_number(check_number, "en")

# print(number_location)
# service_provider = phonenumbers.parse(number)
# service_provider_name = carrier.name_for_number(service_provider, "en")
# print(service_provider_name)
# API_key = "bccab686ab8841a195625e45b1547d61"

# geocoder = OpenCageGeocode(API_key)
# query = str(number_location)
# results = geocoder.geocode(query)
# lat = results[0]['geometry']['lat']
# lng = results[0]['geometry']['lng']

# map_location = folium.Map(location=[lat, lng], zoom_start=9)
# folium.Marker([lat, lng], popup=number_location).add_to(map_location)
# map_location.save(r"C:\Users\avivj\OneDrive\Desktop\aviv\Projects\PhoneNumberTrucker\Location.html")

import phonenumbers
from phonenumbers import geocoder
import folium
from opencage.geocoder import OpenCageGeocode
from phonenumbers import carrier
import requests

# User inputs phone number
number = input("Enter the phone number with country code: ")
check_number = phonenumbers.parse(number)
number_location = geocoder.description_for_number(check_number, "en")

print("Phone Number Approximate Location:", number_location)

# Get service provider
service_provider = phonenumbers.parse(number)
service_provider_name = carrier.name_for_number(service_provider, "en")
print("Service Provider:", service_provider_name)

# OpenCage API Key
API_key = "bccab686ab8841a195625e45b1547d61"
opencage_geocoder = OpenCageGeocode(API_key)

# Use OpenCage to get lat/lng based on city name (less accurate)
query = str(number_location)
results = opencage_geocoder.geocode(query)

if results:
    lat, lng = results[0]['geometry']['lat'], results[0]['geometry']['lng']
    print(f"OpenCage Approximate Coordinates: {lat}, {lng}")
else:
    print("Could not find location via OpenCage.")
    lat, lng = None, None  # Set default values in case of failure

# Try getting more accurate location using IP geolocation
ip_api_url = "http://ip-api.com/json/"
response = requests.get(ip_api_url)
ip_data = response.json()

if ip_data['status'] == 'success':
    ip_lat, ip_lng = ip_data['lat'], ip_data['lon']
    print(f"IP-based More Accurate Location: {ip_lat}, {ip_lng}")
    lat, lng = ip_lat, ip_lng  # Override lat/lng with IP-based location
else:
    print("Could not retrieve IP location. Using OpenCage data.")

# Create map with the best available location
map_location = folium.Map(location=[lat, lng], zoom_start=9)
folium.Marker([lat, lng], popup=f"Estimated Location: {number_location}").add_to(map_location)

# Save map to specified path
save_path = r"C:\Users\avivj\OneDrive\Desktop\aviv\Projects\PhoneNumberTrucker\Location.html"
map_location.save(save_path)

print(f"Map saved successfully at: {save_path}")
