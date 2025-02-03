from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# OpenWeatherMap API Key (use your own API key)
API_KEY = "00a71c6fbbe6d94b622b17d184399db3"  # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

@app.route("/", methods=["GET", "POST"])
def index():
    forecast_data = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            forecast_data = get_forecast(city)
    return render_template("index.html", forecast_data=forecast_data)

def get_forecast(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        daily_forecast = process_forecast(data["list"])
        return daily_forecast
    else:
        return None

def process_forecast(forecast_list):
    daily_forecast = {}
    for entry in forecast_list:
        date = entry["dt_txt"].split(" ")[0]  # Extract the date
        if date not in daily_forecast:
            daily_forecast[date] = {
                "temperature": entry["main"]["temp"],
                "description": entry["weather"][0]["description"],
                "icon": entry["weather"][0]["icon"],
                "humidity": entry["main"]["humidity"],
                "wind_speed": entry["wind"]["speed"]
            }
    # Convert to a list of daily forecasts for the next 4 days
    return list(daily_forecast.values())[:4]

if __name__ == "__main__":
    app.run(debug=True)