import requests
import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

API_KEY = '789c45f216f2e926657548a0fe7e4431'
DEFAULT_CITIES = ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Miami', 'Singapore']
ALERT_LOG_FILE = 'alert_log.txt'
REFRESH_INTERVAL = 300

NOTIFICATION_CONFIG = 'notification_config.txt'


def load_notification_config():
    config = {}
    if os.path.exists(NOTIFICATION_CONFIG):
        with open(NOTIFICATION_CONFIG, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key] = value
    return config


def save_notification_config(config):
    with open(NOTIFICATION_CONFIG, 'w') as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")


def send_email_alert(recipient, subject, body, smtp_server, smtp_port, smtp_user, smtp_password):
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = recipient
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, int(smtp_port))
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipient, msg.as_string())
        server.quit()
        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)


def send_sms_alert(phone, message, twilio_sid, twilio_token, twilio_from):
    try:
        from twilio.rest import Client
        client = Client(twilio_sid, twilio_token)
        client.messages.create(
            body=message,
            from_=twilio_from,
            to=phone
        )
        return True, "SMS sent successfully"
    except ImportError:
        return False, "Twilio not installed. Run: pip install twilio"
    except Exception as e:
        return False, str(e)


def send_notifications(city, rainfall, alert_level):
    config = load_notification_config()
    
    if not config.get('enable_notifications'):
        return
    
    notify_via = config.get('notify_via', 'Email')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    subject = f"⚠️ RAINFLARE ALERT: {city}"
    body = f"""
    RAINFLARE ALERT NOTIFICATION
    ==========================
    City: {city}
    Rainfall: {rainfall} mm/h
    Alert Level: {alert_level}
    Time: {timestamp}
    
    This is an automated alert from the Rainfall Monitor system.
    """
    
    results = []
    
    if notify_via == "Email" and config.get('email') and config.get('smtp_server'):
        success, msg = send_email_alert(
            config['email'],
            subject,
            body,
            config['smtp_server'],
            config.get('smtp_port', '587'),
            config['smtp_user'],
            config['smtp_password']
        )
        results.append(f"Email: {msg}")
    
    if notify_via == "SMS" and config.get('phone') and config.get('twilio_sid'):
        success, msg = send_sms_alert(
            config['phone'],
            f"Rainfall Alert: {city} - {rainfall}mm/h ({alert_level})",
            config['twilio_sid'],
            config['twilio_token'],
            config['twilio_from']
        )
        results.append(f"SMS: {msg}")
    
    return results


def init_session_state():
    """Initialize session state for history storage"""
    if 'history' not in st.session_state:
        st.session_state.history = {}


def fetch_weather(city):
    """
    Fetch current weather data for a given city using OpenWeatherMap API.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        rainfall = data.get('rain', {}).get('1h', 0)
        if rainfall is None:
            rainfall = 0

        weather_info = {
            'city': data.get('name', city),
            'lat': data.get('coord', {}).get('lat', 0),
            'lon': data.get('coord', {}).get('lon', 0),
            'temperature': data.get('main', {}).get('temp', 0),
            'humidity': data.get('main', {}).get('humidity', 0),
            'rainfall': rainfall,
            'description': data.get('weather', [{}])[0].get('description', 'N/A'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return weather_info

    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None


def fetch_all_cities(cities, test_mode=False, test_rainfall=0):
    """
    Fetch weather data for multiple cities.
    """
    results = []
    for city in cities:
        data = fetch_weather(city)
        if data:
            if test_mode:
                data['rainfall'] = test_rainfall
            alert_level, alert_message, alert_color = check_alert(data['rainfall'])
            data['alert_level'] = alert_level
            data['alert_message'] = alert_message
            data['alert_color'] = alert_color
            
            if city not in st.session_state.history:
                st.session_state.history[city] = []
            st.session_state.history[city].append({
                'rainfall': data['rainfall'],
                'temperature': data['temperature'],
                'humidity': data['humidity'],
                'description': data['description'],
                'timestamp': data['timestamp']
            })
            if len(st.session_state.history[city]) > 20:
                st.session_state.history[city] = st.session_state.history[city][-20:]
            
            results.append(data)
    return results


def check_alert(rainfall):
    """
    Implement threshold-based alerting based on rainfall intensity.
    """
    if rainfall >= 20:
        return 'Red', 'Heavy - ALERT', '#FF0000'
    elif rainfall >= 10:
        return 'Yellow', 'Moderate', '#FFFF00'
    else:
        return 'Green', 'Normal', '#00FF00'


def predict_weather_6h(city, current_data=None):
    """
    Predict weather in 6 hours based on current data and trends.
    Returns prediction immediately on first load using current data.
    """
    if city not in st.session_state.history or len(st.session_state.history[city]) < 3:
        if current_data is not None:
            return {
                'rainfall': current_data['rainfall'],
                'temperature': current_data['temperature'],
                'humidity': current_data['humidity'],
                'description': current_data['description']
            }
        return None
    
    recent = st.session_state.history[city][-6:] if len(st.session_state.history[city]) >= 6 else st.session_state.history[city]
    if len(recent) < 3:
        if current_data is not None:
            return {
                'rainfall': current_data['rainfall'],
                'temperature': current_data['temperature'],
                'humidity': current_data['humidity'],
                'description': current_data['description']
            }
        return None
    
    def predict_field(field):
        values = [r[field] for r in recent]
        n = len(values)
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n
        
        numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        intercept = y_mean - slope * x_mean
        predicted = slope * (n + 5) + intercept
        
        if field == 'rainfall':
            predicted = max(0, predicted)
        
        return round(predicted, 1)
    
    pred_rainfall = predict_field('rainfall')
    pred_temp = predict_field('temperature')
    pred_humidity = predict_field('humidity')
    
    descriptions = [r['description'] for r in recent]
    most_common = max(set(descriptions), key=descriptions.count)
    
    return {
        'rainfall': pred_rainfall,
        'temperature': pred_temp,
        'humidity': pred_humidity,
        'description': most_common
    }


def log_alert(rainfall, level, city):
    """
    Your implementation: logging
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] City: {city} | Rainfall: {rainfall} mm/h | Alert: {level}\n"

    with open(ALERT_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)

    return log_entry


def get_colored_status(alert_level, alert_message):
    """Display alert status with proper colors"""
    colors = {
        'Red': ('#FF0000', 'white'),
        'Yellow': ('#FFFF00', 'black'),
        'Green': ('#00FF00', 'black')
    }
    bg_color, text_color = colors.get(alert_level, ('#CCCCCC', 'black'))
    st.markdown(
        f"""
        <div style="background-color: {bg_color}; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="color: {text_color}; margin: 0;">{alert_message}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    """Streamlit dashboard"""
    st.set_page_config(page_title="Rainfall Monitor", page_icon="🌧️", layout="wide")

    init_session_state()

    st_autorefresh(interval=REFRESH_INTERVAL * 1000, key="auto_refresh", debounce=False)

    st.sidebar.title("Settings")

    selected_cities = st.sidebar.multiselect(
        "Select Cities",
        options=['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Chongqing', 'Wuhan', 'Hangzhou', 'Nanjing', 'Miami', 'Singapore', 'Mumbai', 'Hong Kong', 'Bangkok', 'Manila'],
        default=DEFAULT_CITIES
    )

    if not selected_cities:
        selected_cities = DEFAULT_CITIES

    test_mode = st.sidebar.checkbox("Test Mode (simulate alerts)", value=False)
    test_rainfall = 0

    if test_mode:
        st.sidebar.markdown("### Test Rainfall Values")
        test_rainfall = st.sidebar.slider("Simulated Rainfall (mm/h)", 0, 50, 25)

    st.sidebar.divider()

    st.sidebar.info(f"Auto-refresh every {REFRESH_INTERVAL//60} min")

    st.title("Multi-City Rainfall Monitor")

    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("🔄 Refresh", key="refresh_btn_main"):
            st.rerun()

    all_data = fetch_all_cities(selected_cities, test_mode, test_rainfall)

    if all_data:
        df = pd.DataFrame(all_data)
        df = df[['city', 'rainfall', 'alert_level', 'temperature', 'humidity', 'description']]
        df.columns = ['City', 'Rainfall (mm/h)', 'Alert', 'Temp (°C)', 'Humidity (%)', 'Description']

        st.subheader("All Cities Overview")
        st.dataframe(df, use_container_width=True)

        st.subheader("Weather Prediction (6 Hours Ahead)")
        pred_cols = st.columns(len(all_data))
        for i, data in enumerate(all_data):
            pred = predict_weather_6h(data['city'], current_data=data)
            with pred_cols[i]:
                if pred is not None:
                    pred_alert, _, pred_color = check_alert(pred['rainfall'])
                    st.markdown(
                        f"""
                        <div style="background-color: {pred_color}; padding: 15px; border-radius: 10px; text-align: center; margin: 5px 0;">
                            <h4 style="color: {'white' if pred_alert == 'Red' else 'black'}; margin: 0;">{data['city']}</h4>
                            <p style="font-size: 20px; font-weight: bold; color: {'white' if pred_alert == 'Red' else 'black'}; margin: 0;">{pred['rainfall']} mm/h</p>
                            <p style="color: {'white' if pred_alert == 'Red' else 'black'}; margin: 0;">🌡️ {pred['temperature']}°C</p>
                            <p style="color: {'white' if pred_alert == 'Red' else 'black'}; margin: 0;">💧 {pred['humidity']}%</p>
                            <small style="color: {'white' if pred_alert == 'Red' else 'black'};">{pred['description']}</small>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div style="background-color: #CCCCCC; padding: 15px; border-radius: 10px; text-align: center; margin: 5px 0;">
                            <h4 style="color: black; margin: 0;">{data['city']}</h4>
                            <small style="color: black;">Collecting data...</small>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        st.subheader("Alert Notifications")
        config = load_notification_config()
        
        c1, c2 = st.columns([1, 3])
        with c1:
            st.markdown("**Send via:**")
            notify_via = st.segmented_control("Channel", ["Email", "SMS"], 
                default=config.get('notify_via', 'Email'))
        with c2:
            st.markdown("**To:**")
            if notify_via == "SMS":
                phone = st.text_input("Phone", value=config.get('phone', ''), placeholder="+1234567890")
            else:
                email = st.text_input("Email", value=config.get('email', ''), placeholder="email@example.com")

        alerts_triggered = [d for d in all_data if d['alert_level'] == 'Red']
        if alerts_triggered:
            st.warning(f"⚠️ {len(alerts_triggered)} ALERT(S) DETECTED!")
            for alert in alerts_triggered:
                st.write(f"  - {alert['city']}: {alert['rainfall']} mm/h")
                log_alert(alert['rainfall'], alert['alert_level'], alert['city'])
                
                already_notified = st.session_state.get('notified_alerts', set())
                alert_key = f"{alert['city']}_{alert['rainfall']}"
                if alert_key not in already_notified:
                    results = send_notifications(alert['city'], alert['rainfall'], alert['alert_level'])
                    if results:
                        notified_set = st.session_state.get('notified_alerts', set())
                        notified_set.add(alert_key)
                        st.session_state.notified_alerts = notified_set
                        for r in results:
                            st.write(f"  📱 {r}")

        st.sidebar.divider()
        st.sidebar.info(f"Auto-refresh every {REFRESH_INTERVAL//60} minutes")

    else:
        st.error("Unable to fetch weather data. Please check your API key.")


if __name__ == "__main__":
    main()