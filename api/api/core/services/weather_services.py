import requests
import logging
from django.conf import settings

def get_weather_data(lat, long):
    api_url = f"http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}&q={lat},{long}&aqi=no"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return {  # Return a dictionary directly
            'Air temperature': data['current']['temp_c'],
            'precipitation type': get_precipitation_type(data['current']['condition']['code']),
            'precipitation intensity': get_precipitation_intensity(data['current']['precip_mm']),
            'relative humidity': data['current']['humidity'],
            'wind direction': data['current']['wind_degree'],
            'wind speed': data['current']['wind_kph'],
            'Lighting condition': 0 if data['current']['is_day'] == 1 else 2,
            'road condition': determine_road_condition(data['current'])
        }
    else:
        return None  

# function to map codes from weatherapi.com to precipitation types
def get_precipitation_type(weather_code):
    # Classify conditions and map to simplified types
    mapping = {
        # RAIN
        2: [1063, 1072, 1150, 1153, 1168, 1171, 1180, 1183, 1186, 1189, 1192, 1195, 1198, 1201, 1240, 1243, 1246, 1273, 1276],
        # SNOW
        1: [1066, 1069, 1072, 1114, 1117, 1204, 1207, 1210, 1213, 1216, 1219, 1222, 1225, 1255, 1258, 1279, 1282],
        # CLEAR
        0: [1000, 1003, 1006, 1009]  
    } 

    # Find and return the type 
    for precipitation_type, codes in mapping.items():
        if weather_code in codes:
            return precipitation_type

    # Default to "Clear" if nothing matches
    return 0

# function to map precipitation intensity to ml model categories
def get_precipitation_intensity(value):
    if value == 0:
        return 0
    elif value <= 1.0:
        return 1
    elif value <= 5.0:
        return 3
    elif value <= 16.0:
        return 4
    else:
        return 2
    
def determine_road_condition(weather_data):
    # Extract relevant data
    condition_text = weather_data.get("condition", {}).get("text", "").lower()
    temp_c = weather_data.get("temp_c", 0.0)
    has_precipitation = any(word in condition_text 
                            for word in ["rain", "snow", "sleet", "drizzle"])

    # Prioritize precipitation descriptions
    if has_precipitation:
        if "snow" in condition_text:
            return 2
        else:
            return 1

    # Temperature-based conditions
    elif temp_c < 0:
        return 3
    else:
        return 0
