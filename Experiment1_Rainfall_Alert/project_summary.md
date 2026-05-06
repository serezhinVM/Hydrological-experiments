# Rainfall Alert System - Project Summary

## Experiment 1: Rainfall Alert System

### Project Overview
A real-time rainfall monitoring and alert system using OpenWeatherMap API with a Streamlit dashboard.

### Location
`C:\Users\staso\Hydrology_experiments\Experiment1_Rainfall_Alert\`

### API Key
`789c45f216f2e926657548a0fe7e4431`

### Features Implemented

1. **API Integration**
   - OpenWeatherMap API for real-time weather data
   - Multi-city support: Beijing, Shanghai, Guangzhou, Shenzhen, Miami, Singapore

2. **Alert Logic**
   - Green: Rainfall < 10 mm/h (Normal)
   - Yellow: 10 ≤ Rainfall < 20 mm/h (Moderate)
   - Red: Rainfall ≥ 20 mm/h (Heavy - ALERT)

3. **Test Mode**
   - Slider to simulate rainfall (0-50 mm/h) for testing alert triggers

4. **Weather Prediction**
   - 6-hour forecast based on current data
   - Shows: Rainfall, Temperature, Humidity, Description

5. **Email/SMS Notifications**
   - Email via SMTP (Gmail supported)
   - SMS via Twilio
   - Notification settings on main page

6. **Auto-refresh**
   - 5-minute interval

### Files
- `weather_monitor.py` - Main application
- `alert_log.txt` - Alert event log
- `prompt_log.md` - AI interactions documentation
- `test_cities.py` - Test script
- `check_rain.py` - Rain data check
- `find_rain.py` - Find cities with rain

### How to Run
```bash
streamlit run weather_monitor.py
```

### Dashboard Sections
1. **All Cities Overview** - DataFrame with city weather data
2. **Weather Prediction (6 Hours Ahead)** - Forecast cards
3. **Alert Notifications** - Email/SMS configuration

### Auto-refresh
- Interval: 300 seconds (5 minutes)
- Manual refresh button on main page

### Notes
- OpenWeatherMap API returns 0 mm/h when not raining
- Test Mode enables alert testing without real rain
- Predictions appear immediately using current data

---
*Generated: 2026-04-28*