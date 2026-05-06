import requests

API_KEY = '789c45f216f2e926657548a0fe7e4431'
cities = ['London', 'Tokyo', 'Miami', 'Seattle', 'Singapore', 'Mumbai', 'Hong Kong']

print("Checking rainfall data from various cities:")
for c in cities:
    r = requests.get('https://api.openweathermap.org/data/2.5/weather', params={'q': c, 'appid': API_KEY, 'units': 'metric'}, timeout=10)
    data = r.json()
    rain = data.get('rain', {})
    rain_1h = rain.get('1h', 0) if rain else 0
    weather = data.get('weather', [{}])[0].get('description', 'N/A')
    print(f"{c}: rain_1h={rain_1h} mm, weather={weather}")