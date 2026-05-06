import requests

API_KEY = '789c45f216f2e926657548a0fe7e4431'

def check_alert(rainfall):
    if rainfall >= 20:
        return 'Red', 'Heavy - ALERT'
    elif rainfall >= 10:
        return 'Yellow', 'Moderate'
    else:
        return 'Green', 'Normal'

test_cases = [0, 5, 10, 15, 20, 25]
print("Testing Alert Logic:")
print("-" * 40)
for rainfall in test_cases:
    level, status = check_alert(rainfall)
    print(f"Rainfall: {rainfall} mm/h -> {level}: {status}")

print("\nValidation: Alerts trigger at correct thresholds:")
print(f"  Rainfall < 10:  {check_alert(9)[0]} (expected Green)")
print(f"  10 <= Rainfall < 20: {check_alert(10)[0]} (expected Yellow)")
print(f"  Rainfall >= 20: {check_alert(20)[0]} (expected Red)")