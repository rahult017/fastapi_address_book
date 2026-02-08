import uvicorn

from typing import List
from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from .database import init_db, get_session, get_db
from .config import settings
from .logger import logger
from . import schemas, crud
from .geo_service import GeoService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Starting Address Service API")

    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down Address Service API")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_model=schemas.HealthCheck,
)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
        return schemas.HealthCheck(
            status="healthy",
            version=settings.VERSION,
            database=db_status,
            timestamp=datetime.utcnow(),
        )
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}",
        )


@app.post(
    "/addresses",
    summary="Create a new address",
    description="Create a new address with validation of coordinates and address data",
    response_model=schemas.AddressRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_address(
    address_in: schemas.AddressCreate,
    db: Session = Depends(get_session),
):
    logger.info("Creating address: %s", address_in.dict())
    try:
        created = crud.create_address(db, address_in)
        logger.info(f"Address created successfully {create_address}")
        return created
    except Exception as e:
        logger.error(f"Failed to create address: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.get(
    "/addresses",
    response_model=schemas.AddressResponse,
    summary="Get all addresses",
    description="Retrieve paginated list of all addresses",
    status_code=status.HTTP_200_OK,
)
async def read_addresses(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db),
):
    """Get paginated list of addresses"""
    logger.info(f"Fetching addresses page {page}, size {size}")

    try:
        skip = (page - 1) * size
        addresses, total = crud.get_addresses(db, skip=skip, limit=size)
        logger.info("Address fetch successfully {addresses}")
        return schemas.AddressResponse(
            items=addresses,
            total=total,
            page=page,
            size=size,
        )
    except Exception as e:
        logger.error(f"Failed to fetch addresses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve addresses",
        )


@app.get(
    "/addresses/{address_id}",
    summary="Get address by ID",
    description="Retrieve a specific address by its ID",
    response_model=schemas.AddressResponse,
    status_code=status.HTTP_200_OK,
)
async def read_address(address_id: int, db: Session = Depends(get_session)):
    try:
        logger.info(f"Fetching address with ID {address_id}")
        addr = crud.get_address(db, address_id)
        logger.info(f"Fetching address with ID {addr}")
        if not addr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found",
            )
        return addr
    except Exception as e:
        logger.error(f"Failed to fetch addresses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve addresses",
        )


@app.patch(
    "/addresses/{address_id}",
    summary="Update an address",
    description="Update an existing address by ID",
    response_model=schemas.AddressRead,
    status_code=status.HTTP_200_OK,
)
async def patch_address(
    address_id: int,
    address_in: schemas.AddressUpdate,
    db: Session = Depends(get_session),
):
    try:
        logger.info(f"Updating address with ID {address_id}")
        updated = crud.update_address(db, address_id, address_in)
        logger.info(f"Addresses updated successfully {updated}")
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found",
            )
        return updated
    except Exception as e:
        logger.error(f"Failed to updated addresses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to updated addresses",
        )


@app.delete(
    "/addresses/{address_id}",
    summary="Delete an address",
    description="Delete an address by ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_address(address_id: int, db: Session = Depends(get_session)):
    try:
        logger.info(f"Deleting address with ID {address_id}")
        success = crud.delete_address(db, address_id)
        logger.info(f"Deleting addresses  {success}")
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found",
            )
        return None
    except Exception as e:
        logger.error(f"Failed to updated addresses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to updated addresses",
        )


@app.get(
    "/addresses/nearby",
    response_model=List[schemas.AddressRead],
    status_code=status.HTTP_200_OK,
)
async def addresses_nearby(
    latitude: float = Query(..., description="Latitude of the search center"),
    longitude: float = Query(..., description="Longitude of the search center"),
    radius_km: float = Query(5.0, gt=0, description="Search radius in kilometers"),
    limit: int = Query(20, gt=0, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_session),
):
    logger.info(
        "Searching addresses near (%s, %s) radius=%s km", latitude, longitude, radius_km
    )

    rows = crud.list_addresses_nearby(
        db, latitude, longitude, radius_km, limit=limit, offset=offset
    )

    # Return only the address objects
    return [r["address"] for r in rows]


@app.get(
    "/addresses/{address_id}/distance",
    summary="Calculate distance between addresses",
    description="Calculate distance from one address to another",
    status_code=status.HTTP_200_OK,
)
async def calculate_distance(
    address_id: int,
    target_latitude: float = Query(..., ge=-90, le=90),
    target_longitude: float = Query(..., ge=-180, le=180),
    db: Session = Depends(get_db),
):
    """Calculate distance from address to target coordinates"""
    logger.info(
        f"Calculating distance from address {address_id} "
        f"to ({target_latitude}, {target_longitude})"
    )

    db_address = crud.get_address(db, address_id=address_id)
    if db_address is None:
        logger.warning(
            f"Address with ID {address_id} not found for distance calculation"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )

    try:
        distance = GeoService.calculate_distance(
            db_address.latitude, db_address.longitude, target_latitude, target_longitude
        )

        return {
            "from_address": {
                "id": db_address.id,
                "latitude": db_address.latitude,
                "longitude": db_address.longitude,
            },
            "to_coordinates": {
                "latitude": target_latitude,
                "longitude": target_longitude,
            },
            "distance_km": distance,
        }
    except Exception as e:
        logger.error(f"Failed to calculate distance: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post(
    "/addresses/search",
    response_model=List[schemas.AddressSearchResult],
    summary="Search addresses by distance",
    description="Search for addresses within a given distance from coordinates",
    status_code=status.HTTP_200_OK,
)
async def search_addresses(
    search_query: schemas.AddressSearchQuery, db: Session = Depends(get_db)
):
    """Search addresses within distance from coordinates"""
    logger.info(
        f"Searching addresses within {search_query.distance_km}km "
        f"of ({search_query.latitude}, {search_query.longitude})"
    )

    try:
        results = crud.search_addresses_within_distance(
            db=db, search_query=search_query
        )

        return [
            schemas.AddressSearchResult(address=address, distance_km=distance)
            for address, distance in results
        ]
    except Exception as e:
        logger.error(f"Failed to search addresses: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    uvicorn.run(
        "apps.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
