import requests
import streamlit as st
from datetime import datetime
import time
import pandas as pd
import os
import pydeck as pdk

API_KEY = '789c45f216f2e926657548a0fe7e4431'
CITIES = ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Wuhan']
API_ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather'

CITY_COORDS = {
    'Beijing': (39.9042, 116.4074),
    'Shanghai': (31.2304, 121.4737),
    'Guangzhou': (23.1291, 113.2644),
    'Shenzhen': (22.5431, 114.0579),
    'Wuhan': (30.5928, 114.3055),
}

ALERT_COLORS = {
    'Green': [0, 180, 0],
    'Yellow': [255, 200, 0],
    'Red': [220, 0, 0],
}

st.set_page_config(page_title='Rainfall Monitor - Multi City', layout='wide')

def fetch_weather(city):
    """Fetch current weather data from OpenWeatherMap API."""
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(API_ENDPOINT, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        rainfall = 0
        if 'rain' in data:
            if '1h' in data['rain']:
                rainfall = data['rain']['1h']
            elif '3h' in data['rain']:
                rainfall = data['rain']['3h'] / 3

        return {
            'city': data.get('name', city),
            'temperature': data.get('main', {}).get('temp', 0),
            'humidity': data.get('main', {}).get('humidity', 0),
            'rainfall': rainfall,
            'description': data.get('weather', [{}])[0].get('description', 'N/A'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except requests.exceptions.RequestException as e:
        return {'error': str(e), 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'city': city}

def check_alert(rainfall):
    """Determine alert level based on rainfall intensity."""
    if rainfall < 10:
        return 'Green', 'Normal', 'rgba(0, 255, 0, 0.3)'
    elif rainfall < 20:
        return 'Yellow', 'Moderate', 'rgba(255, 255, 0, 0.3)'
    else:
        return 'Red', 'Heavy - ALERT', 'rgba(255, 0, 0, 0.3)'

def log_alert(rainfall, level, status, city):
    """Log alert event to file with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {city}: {level} - {status} (Rainfall: {rainfall:.2f} mm/h)\n"

    with open('alert_log.txt', 'a') as f:
        f.write(log_entry)

    return log_entry

def get_rainfall_category(rainfall):
    """Return rainfall category based on China Meteorological Administration standards."""
    if rainfall < 10:
        return "Light rain / Moderate rain"
    elif rainfall < 20:
        return "Heavy rain"
    elif rainfall < 50:
        return "Torrential rain"
    else:
        return "Heavy torrential rain / Extreme rainfall"

def main():
    title_col, btn_col = st.columns([4, 1])
    with title_col:
        st.title('Rainfall Monitor - Multi City')
    with btn_col:
        st.write('')
        if st.button('Refresh All Data', use_container_width=True):
            st.rerun()
    st.markdown('---')

    if 'history' not in st.session_state:
        st.session_state.history = {}

    for city in CITIES:
        if city not in st.session_state.history:
            st.session_state.history[city] = []

    all_data = {}
    errors = []

    for city in CITIES:
        weather_data = fetch_weather(city)
        if 'error' in weather_data:
            errors.append(weather_data)
        else:
            all_data[city] = weather_data
            st.session_state.history[city].append(weather_data)
            if len(st.session_state.history[city]) > 50:
                st.session_state.history[city] = st.session_state.history[city][-50:]

    if errors:
        with st.expander('API Errors'):
            for err in errors:
                st.error(f"{err['city']}: {err['error']}")

    st.subheader('Weather Map')
    map_data = pd.DataFrame([
        {
            'lat': CITY_COORDS[city][0],
            'lon': CITY_COORDS[city][1],
            'rainfall': d['rainfall'],
            'color': ALERT_COLORS[check_alert(d['rainfall'])[0]],
            'city': d['city'],
            'alert': check_alert(d['rainfall'])[0],
        }
        for city, d in all_data.items() if city in CITY_COORDS
    ])

    if not map_data.empty:
        view_state = pdk.ViewState(
            latitude=map_data['lat'].mean(),
            longitude=map_data['lon'].mean(),
            zoom=4.5,
            pitch=0,
        )
        map_data['stroke_color'] = [[0, 0, 0, 180]] * len(map_data)
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=map_data,
            get_position='[lon, lat]',
            get_color='color',
            get_radius=30000,
            radius_min_pixels=8,
            radius_max_pixels=20,
            get_line_color='stroke_color',
            get_line_width=2,
            pickable=True,
            tooltip={
                'html': '<b>{city}</b><br/>Rainfall: {rainfall} mm/h<br/>Alert: {alert}',
                'style': {'backgroundColor': 'steelblue', 'color': 'white'},
            },
        )
        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={'text': '{city}: {rainfall} mm/h'},
        ))

    legend_html = '<div style="display:flex; gap:20px; justify-content:center; padding:5px;">'
    for level, rgb in ALERT_COLORS.items():
        legend_html += (
            f'<span style="display:inline-flex; align-items:center; gap:5px;">'
            f'<span style="width:16px;height:16px;border-radius:50%;'
            f'background:rgb({rgb[0]},{rgb[1]},{rgb[2]});display:inline-block;"></span>'
            f'{level}</span>'
        )
    legend_html += '</div>'
    st.markdown(legend_html, unsafe_allow_html=True)

    cols = st.columns(len(CITIES))
    for idx, city in enumerate(CITIES):
        if city not in all_data:
            continue
        data = all_data[city]
        level, status, color = check_alert(data['rainfall'])

        with cols[idx]:
            st.subheader(f'📍 {data["city"]}')
            st.metric(label='Rainfall', value=f"{data['rainfall']:.2f} mm/h")
            st.markdown(
                f'<div style="background: {color}; padding: 15px; border-radius: 10px; '
                f'text-align: center; font-size: 20px; font-weight: bold;">'
                f'{level}: {status}</div>',
                unsafe_allow_html=True
            )
            st.caption(f"Category: {get_rainfall_category(data['rainfall'])}")
            st.write(f"**Temp:** {data['temperature']}°C")
            st.write(f"**Humidity:** {data['humidity']}%")
            st.write(f"**Condition:** {data['description'].capitalize()}")

            if level == 'Red':
                log_alert(data['rainfall'], level, status, data['city'])
                st.warning(f"ALERT: Heavy rainfall! ({data['rainfall']:.2f} mm/h)")

if __name__ == '__main__':
    main()
