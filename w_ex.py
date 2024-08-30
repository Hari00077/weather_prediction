import streamlit as st
import requests

# Title of the app
st.title("Weather Prediction")

# Input field for location
location = st.text_area("Enter location:")

def find_key(location):
    # Define the API key and base URL
    api_key = "8OqRWQWlg80Ni0noXfiKhmTWwpkJRdKQ"
    base_url = "http://dataservice.accuweather.com/locations/v1/cities/search"

    try:
        # Make the API request
        response = requests.get(f"{base_url}?apikey={api_key}&q={location}")
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Process the response
        data = response.json()
        if data:
            key = data[0]['Key']  # Extract the first result's key
            return key
        else:
            st.error("No locations found. Please try a different search.")
            return None
    except requests.RequestException as e:
        st.error(f"Failed to retrieve data: {e}")
        return None

def get_forecast(location):
    key = find_key(location)
    if not key:
        return None

    api_key = "8OqRWQWlg80Ni0noXfiKhmTWwpkJRdKQ"
    forecast_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{key}?apikey={api_key}&metric=true"

    try:
        # Make the API request for the forecast
        response = requests.get(forecast_url)
        response.raise_for_status()

        # Process the forecast data
        forecast_data = response.json()
        return forecast_data
    except requests.RequestException as e:
        st.error(f"Failed to retrieve forecast data: {e}")
        return None

if st.button("Find Weather"):
    if location:
        forecast_data = get_forecast(location)
        if forecast_data:
            st.write(f"5-Day Weather Forecast for '{location}':")
            for day in forecast_data['DailyForecasts']:
                date = day['Date']
                min_temp = day['Temperature']['Minimum']['Value']
                max_temp = day['Temperature']['Maximum']['Value']
                condition = day['Day']['IconPhrase']
                st.write(f"{date}: Condition: {condition}, Min Temp: {min_temp}°C, Max Temp: {max_temp}°C")
    else:
        st.warning("Please enter a location.")
