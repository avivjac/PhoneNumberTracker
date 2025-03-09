from flask import Flask, render_template, request, jsonify
import phonenumbers
from phonenumbers import geocoder, carrier
import folium
from opencage.geocoder import OpenCageGeocode
import os

app = Flask(__name__)
API_KEY = "bccab686ab8841a195625e45b1547d61"  # Replace with your actual OpenCage API key

def get_phone_info(number):
    try:
        check_number = phonenumbers.parse(number)
        number_location = geocoder.description_for_number(check_number, "en")
        service_provider = carrier.name_for_number(check_number, "en")
        return number_location, service_provider
    except Exception as e:
        print(f"Error in get_phone_info: {e}")
        return None, None

def get_coordinates(location):
    try:
        geocoder = OpenCageGeocode(API_KEY)
        results = geocoder.geocode(location)
        if results:
            return results[0]['geometry']['lat'], results[0]['geometry']['lng']
    except Exception as e:
        print(f"Error in get_coordinates: {e}")
    return None, None

def generate_map(lat, lng, location):
    try:
        map_location = folium.Map(location=[lat, lng], zoom_start=9)
        folium.Marker([lat, lng], popup=location).add_to(map_location)
        map_path = "static/Location.html"
        map_location.save(map_path)
        return map_path
    except Exception as e:
        print(f"Error in generate_map: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        number = request.form.get('phone_number')
        location, provider = get_phone_info(number)
        if location:
            lat, lng = get_coordinates(location)
            if lat and lng:
                map_path = generate_map(lat, lng, location)
                return render_template('ClientSide.html', location=location, provider=provider, map_path=map_path)
        return render_template('ClientSide.html', error="Could not retrieve location.")
    return render_template('ClientSide.html')

if __name__ == '__main__':
    app.run(debug=True)
