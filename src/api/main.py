import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import schemas.location_schemas as schemas
from db import engine
from logger import logger
from routers.location_router import router as location_router
from routers.forecast_router import router as forecast_router


app = FastAPI()
logger.info("Starting the app...")



# register middlewares

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

schemas.Base.metadata.create_all(bind=engine) # Create the tables 

app.include_router(location_router)
app.include_router(forecast_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)