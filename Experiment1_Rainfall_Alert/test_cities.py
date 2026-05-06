import sys
sys.path.insert(0, r'C:\Users\staso\Hydrology_experiments\Experiment1_Rainfall_Alert')
from weather_monitor import fetch_all_cities

data = fetch_all_cities(['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen'])
for d in data:
    print(f"{d['city']}: {d['rainfall']} mm/h ({d['alert_level']})")