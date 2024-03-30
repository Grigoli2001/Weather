from fastapi import APIRouter, HTTPException, status
from logger import logger
import schemas.location_schemas as schemas
import basemodels.location_basemodels as basemodels
from utils.utils import db_dependency, fetch_weather, get_lat_lon

router = APIRouter()

@router.get("/search/{location}", status_code=status.HTTP_200_OK)
async def search_location(location: str):
    if len(location.strip()) <= 2:
        raise HTTPException(status_code=400, detail="Search query must be at least 3 characters long")
    lat_lon = get_lat_lon(location)
    return lat_lon
            
@router.get("/locations/", status_code=status.HTTP_200_OK, response_model=list[basemodels.LocationBase])
async def get_locations(db: db_dependency):
    locations = db.query(schemas.Location).all()
    # Reverse the list of locations
    locations = locations[::-1]
    for location in locations:
        try:
            weather = fetch_weather(location.latitude, location.longitude)
            location.weather = weather
        except Exception as e:
            location.weather = None

    return locations


    

@router.post("/locations/", status_code=status.HTTP_201_CREATED)
async def create_location(location_data: basemodels.LocationCreate, db: db_dependency):
    location = basemodels.LocationBase(name=location_data.name)
    location.weather = None
    lat_lon = get_lat_lon(location.name)
    if len(lat_lon) == 0:
        raise HTTPException(status_code=404, detail="Location not found")
    elif len(lat_lon) > 1:
        raise HTTPException(status_code=300, detail={"variants": lat_lon})
    
    # changing name, latitude and longitude to the values from the csv file
    location.name = lat_lon[0][0]
    location.latitude = float(lat_lon[0][1])
    location.longitude = float(lat_lon[0][2])

    # Get latitude and longitude from csv file
    new_location = schemas.Location(**location.model_dump())
    try:
        db.add(new_location)
        db.commit()
        db.refresh(new_location)
        
        # fetch weather data
        new_location.weather = fetch_weather(new_location.latitude, new_location.longitude)

        return new_location
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the location")

@router.delete("/locations/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(location_id: int, db: db_dependency):
    location = db.query(schemas.Location).filter(schemas.Location.id == location_id).first()
    if location:
        db.delete(location)
        db.commit()
        return
    raise HTTPException(status_code=404, detail="Location not found")

