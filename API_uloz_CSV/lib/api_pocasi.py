import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

def stahni_pocasi():
    """Stahne data o pocasi z Open-Meteo API a vrati DataFrame."""
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # vezme to API s moji lokaci, vezme teplotu, vitr pri 975hPa a predpoved deste
    # (nekde v zavorce ve vysvetlivkach to odpovidalo 380m nad morem 
    # a tedy priblizne nadmorske vysce lokace... proto takto vybrano)
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 49.5368,
        "longitude": 18.0597,
        "hourly": ["temperature_975hPa", "wind_speed_975hPa", "rain"],
        "timezone": "Europe/Berlin",
    }
    # Vyber dat z API
    
    responses = openmeteo.weather_api(url, params = params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_temperature_975hPa = hourly.Variables(0).ValuesAsNumpy()
    hourly_wind_speed_975hPa = hourly.Variables(1).ValuesAsNumpy()
    hourly_rain = hourly.Variables(2).ValuesAsNumpy()

    # vytvor data pro graf pomoci pandas
    hourly_data = {"Datum": pd.date_range(
        start = pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
        end =  pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    # prirazeni dat
    hourly_data["Teplota"] = hourly_temperature_975hPa
    hourly_data["Vitr"] = hourly_wind_speed_975hPa
    hourly_data["Dest"] = hourly_rain

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    return hourly_dataframe 