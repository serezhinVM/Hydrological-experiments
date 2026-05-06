# AI Interactions Prompt Log

## Experiment 1: Rainfall Alert System

### Session Date: 2026-04-28

### AI Interactions

#### Interaction 1: Initial Code Generation
**Prompt:**
> I am a water resources student building a rainfall monitoring system. Please write Python code to fetch current weather data for Beijing using the OpenWeatherMap API. The code should:
> 1. Use the requests library to make the API call
> 2. Extract rainfall intensity from the response
> 3. Handle API errors gracefully
> 4. Include comments explaining each step
> API endpoint: https://api.openweathermap.org/data/2.5/weather

**Response:** AI generated complete weather fetching function with error handling.

#### Interaction 2: Alert Logic Implementation
**Prompt:**
> Implement threshold-based alerting for rainfall:
> - Green: Rainfall < 10 mm/h (Normal)
> - Yellow: 10 ≤ Rainfall < 20 mm/h (Moderate)
> - Red: Rainfall ≥ 20 mm/h (Heavy - ALERT)

**Response:** AI provided the check_alert function with proper threshold logic.

#### Interaction 3: Dashboard Structure
**Prompt:**
> Build a Streamlit dashboard for rainfall monitoring with:
> - Title: 'Rainfall Monitor - [City Name]'
> - Current rainfall display (large metric)
> - Alert status indicator (color-coded)
> - Auto-refresh capability

**Response:** AI provided complete dashboard code with Streamlit components.

### Errors Found and Corrections Made

1. **Initial rainfall value handling**: Initially the API might return None for rainfall if there's no rain. Fixed by adding: `if rainfall is None: rainfall = 0`

2. **Color contrast**: Adjusted color codes to ensure text readability (white text for red background).

3. **Streamlit auto-refresh**: Used st.rerun() with auto-refresh implementation.

### Notes
- The free OpenWeather tier has rate limits (60 calls/min)
- If API returns 0 rainfall, it might not be raining (expected behavior)
- Always verify AI-generated code handles errors gracefully