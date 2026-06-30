import requests

API_URL="https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"


def obtener_apiclima():
    response = requests.get(API_URL, timeout=10)
    
    if response.status_code == 200:
        return response.json()
    else:
        return[]