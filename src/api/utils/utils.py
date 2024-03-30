import csv
from fastapi import HTTPException, Depends
from logger import logger
from db import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import datetime
# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency =  Annotated[Session, Depends(get_db)]


def fetch_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	"latitude": latitude,
	"longitude": longitude,
	"current": ["temperature_2m", "precipitation", "weather_code"],
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"]
    }
    try:
        responses = openmeteo.weather_api(url, params=params)
        response =  responses[0]
        daily_times = response.Daily().Time()
        daily_times_end= response.Daily().TimeEnd()
        print(daily_times)
        dt_start_object = datetime.datetime.fromtimestamp(daily_times, tz=datetime.timezone.utc)
        dt_end_object = datetime.datetime.fromtimestamp(daily_times_end, tz=datetime.timezone.utc)
        # generate dates between start and end
        daily_times = pd.date_range(start=dt_start_object, end=dt_end_object, freq='D').strftime('%Y-%m-%d').tolist()
        print(daily_times)

        response_dict = {
            "latitude": response.Latitude(),
            "longitude": response.Longitude(),
            "utc_offset_seconds": response.UtcOffsetSeconds(),
            "current": {
                "time": response.Current().Time(),
                "temperature_2m": response.Current().Variables(0).Value(),
                "precipitation": response.Current().Variables(1).Value(),
                "weather_code": response.Current().Variables(2).Value()
            },
            "daily": {
                "time": daily_times,
                "weather_code": response.Daily().Variables(0).ValuesAsNumpy().tolist(),
                "temperature_2m_max": response.Daily().Variables(1).ValuesAsNumpy().tolist(),
                "temperature_2m_min": response.Daily().Variables(2).ValuesAsNumpy().tolist(),
            }
        }

        return response_dict
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the weather data")
    

def get_lat_lon(location):
    # Get latitude and longitude from csv file
    results = [] # List of tuples (there can be multiple results for a search query)
    try:
        with open('country-capital-lat-long-population.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            if len(location.strip()) <= 2:
                return results
            for row in reader:
                country = row[0].lower().strip()
                city = row[1].lower().strip()
                # Implement a seach by country or city
                if location.lower().strip() in country or location.lower().strip() in city:
                    results.append((row[1], row[2], row[3]))
    except FileNotFoundError:
        print("Error: CSV file not found.")
    except Exception as e:
        print("An error occurred:", e)
    return results
