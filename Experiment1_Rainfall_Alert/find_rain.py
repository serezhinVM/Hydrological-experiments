import requests

API_KEY = '789c45f216f2e926657548a0fe7e4431'
cities = [
    'Kolkata', 'Chennai', 'Jakarta', 'Kuala Lumpur', 'Manila', 
    'Colombo', 'Rio de Janeiro', 'Salvador', 'Recife',
    'Cancun', 'San Juan', 'Panama City', 'Ho Chi Minh City'
]

print("Finding cities with higher rainfall:")
results = []
for c in cities:
    try:
        r = requests.get('https://api.openweathermap.org/data/2.5/weather', params={'q': c, 'appid': API_KEY, 'units': 'metric'}, timeout=10)
        data = r.json()
        rain = data.get('rain', {}).get('1h', 0) or 0
        weather = data.get('weather', [{}])[0].get('description', 'N/A')
        results.append((c, rain, weather))
    except:
        pass

results.sort(key=lambda x: x[1], reverse=True)
for c, rain, weather in results[:10]:
    level = 'Red' if rain >= 20 else 'Yellow' if rain >= 10 else 'Green'
    print(f"{c}: {rain} mm/h - {weather} ({level})")