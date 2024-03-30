from fastapi import APIRouter, HTTPException, status
from logger import logger
import schemas.location_schemas as models
from utils.utils import db_dependency, fetch_weather, get_lat_lon
import requests

router = APIRouter()


@router.get("/forecast/{location_id}", status_code=status.HTTP_200_OK)
async def get_forecast(location_id: int, db: db_dependency):
    location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if location:
        try:
            weather = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&daily=temperature_2m_max,temperature_2m_min,weather_code')
            return weather.json()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail="An error occurred while fetching the weather data")
    raise HTTPException(status_code=404, detail="Location not found")
