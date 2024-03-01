import requests
import logging
from django.conf import settings

def get_weather_data(lat, long, hours):
    api_url = "http://api.weatherapi.com/v1/history.json?key={key}&q={lat},{long}&dt={date}"

    weather_data = [] 

    # Determine the unique dates we need data for
    dates = sorted({hour.date() for hour in hours})

    # Make at most two API requests, one for each date
    for date in dates[:2]:  
        date_str = date.strftime('%Y-%m-%d')

        response = requests.get(api_url.format(date=date_str, lat=lat, long=long, key=settings.WEATHER_API_KEY))

        if response.status_code == 200:
            data = response.json()
            hour_data = data.get('forecast', {}).get('forecastday', [{}])[0].get('hour')

            # Process all hours that fall on this date
            for hour in hours:
                if hour.date() == date:  # Only process if the hour belongs to this date
                    target_hour = hour.strftime("%H")

                    # Find matching hour or use previous data
                    for entry in hour_data:
                        if entry['time'].split()[1] == target_hour + ':00':
                            weather_data.append({  
                                'Air temperature': entry['temp_c'],
                                'precipitation type': get_precipitation_type(entry['condition']['code']),
                                'precipitation intensity': get_precipitation_intensity(entry['precip_mm']),
                                'relative humidity': entry['humidity'],
                                'wind direction': entry['wind_degree'],
                                'wind speed': entry['wind_kph'],
                                'Lighting condition': 0 if entry['is_day'] == 1 else 2,
                                'road condition': determine_road_condition(entry),
                                'hour': hour
                            })
                            break  
                    else:
                        if  weather_data: 
                            weather_data.append(weather_data[-1]) 
                        else:
                            # Handle missing data for the first hour
                            pass

    return weather_data 

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
