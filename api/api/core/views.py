from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .services.ml_models import model, prepare_data
from .services.weather_services import get_weather_data
import datetime
from .models import Trip, Driver
from .serializers import TripSerializer
import logging
import json

class TripView(APIView):
    def post(self, request):
        try:
            data_str = request.body.decode('utf-8')  # Decode bytes into a string
            data = json.loads(data_str)            # Parse the JSON string
        except Exception as e:
            logging.error(f'Error parsing JSON: {e}')
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        driver = Driver(name="Alice", vehicle_length=1265, vehicle_weight=10243, axles_number=2)

        start_time = None
        weather_info = None

        trip = Trip(normal_entries=0, vague_entries=0, dangerous_entries=0, driver=driver)

        for entry in data:
            timestamp = datetime.datetime.fromisoformat(entry.get('time'))

            # Calculate 5-minute bucket
            five_minute_bucket = (timestamp.minute // 5) * 5

            if start_time is None or five_minute_bucket != start_time.minute:
                start_time = timestamp
                weather_info = get_weather_data(entry['longitude'], entry['latitude'])

            del entry['longitude']
            del entry['latitude']
            del entry['time']

            entry["axles number"] = driver.axles_number
            entry["vehicle length"] = driver.vehicle_length
            entry["vehicle weight"] = driver.vehicle_weight

            entry.update(weather_info)

            # Prepare the data for the model
            data = prepare_data(entry)

            # Apply your scikit-learn model 
            prediction = model.predict(data)
            if prediction == 2:
                trip.normal_entries += 1
            elif prediction == 1:
                trip.dangerous_entries += 1
            else:
                trip.vague_entries += 1
        
        trip.save()

        serializer = TripSerializer(trip)
        return JsonResponse(serializer.data, status=201)
