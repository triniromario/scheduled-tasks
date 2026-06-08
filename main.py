import requests
import os
from twilio.rest import Client

MY_LAT = 50.4478813 # Your latitude
MY_LONG = -104.6056188 # Your longitude
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

# Pass your actual Twilio credentials directly as strings
api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

parameters = {
        'lat': MY_LAT,
        'lon': MY_LONG,
        'appid': api_key,
        'cnt': 4,
    }

try:
    response = requests.get(OWM_Endpoint, params=parameters)
    response.raise_for_status()
    weather_data = response.json()
    print(weather_data)

except requests.exceptions.RequestException as e:
    print(f"Network error")

# 1. Look for the key "list" (NOT "hourly")
forecast_list = weather_data["list"]

will_rain = False

# 2. Loop through the 4 items the API sent back
for hour_data in forecast_list:
    # Dig into the weather dictionary item
    condition_code = hour_data["weather"][0]["id"]

    # Under 700 means rain/snow/storm
    if condition_code < 700:
        will_rain = True

# 3. Make your decision
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today.",
        from_="+16479312291",
        to="3065528822",)
    print(message.status)
else:
    print("No rain expected in the next 12 hours.")


