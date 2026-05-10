# Experiment 1: Rainfall Alert System

Real-time rainfall monitoring dashboard for 5 Chinese cities (Beijing, Shanghai, Guangzhou, Shenzhen, Wuhan).

## Overview

- **Streamlit dashboard** (`weather_monitor.py`) — displays rainfall, temperature, humidity data
- **OpenWeatherMap API integration** — real-time weather data fetching
- **Color-coded alert system:**
  - 🟢 Green (< 10 mm/h) — normal
  - 🟡 Yellow (10–20 mm/h) — moderate
  - 🔴 Red (≥ 20 mm/h) — heavy rainfall, logged to file
- **Interactive map** using pydeck with color-coded alert levels
- **CMA classification** (China Meteorological Administration standards)
- **Alert logging** to `alert_log.txt`
- **History tracking** (up to 50 records per city via session state)

## Files

| File | Purpose |
|------|---------|
| `weather_monitor.py` | Main dashboard script |
| `alert_log.txt` | Alert event log |
| `Experiment1_Rainfall_Alert.docx` | Experiment description |
| `prompt_log.md` | AI interaction log |
| `Webpage_screenshot.jpg` | Dashboard screenshot |
