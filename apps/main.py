from typing import List
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .database import init_db, get_session
from .config import settings
from .logger import logger
from . import schemas, crud


app = FastAPI(title=settings.APP_NAME)


@app.on_event("startup")
def on_startup():
    logger.info("Initializing database and tables...")
    init_db()


@app.post("/addresses", response_model=schemas.AddressRead, status_code=201)
def create_address(
    address_in: schemas.AddressCreate,
    db: Session = Depends(get_session)
):
    logger.info("Creating address: %s", address_in.dict())
    created = crud.create_address(db, address_in)
    return created


@app.get("/addresses/{address_id}", response_model=schemas.AddressRead)
def read_address(address_id: int, db: Session = Depends(get_session)):
    addr = crud.get_address(db, address_id)
    if not addr:
        raise HTTPException(status_code=404, detail="Address not found")
    return addr


@app.patch("/addresses/{address_id}", response_model=schemas.AddressRead)
def patch_address(
    address_id: int,
    address_in: schemas.AddressUpdate,
    db: Session = Depends(get_session)
):
    updated = crud.update_address(db, address_id, address_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Address not found")
    return updated


@app.delete("/addresses/{address_id}", status_code=204)
def delete_address(address_id: int, db: Session = Depends(get_session)):
    success = crud.delete_address(db, address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")


@app.get("/addresses/nearby", response_model=List[schemas.AddressRead])
def addresses_nearby(
    latitude: float = Query(..., description="Latitude of the search center"),
    longitude: float = Query(..., description="Longitude of the search center"),
    radius_km: float = Query(5.0, gt=0, description="Search radius in kilometers"),
    limit: int = Query(20, gt=0, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_session)
):
    logger.info(
        "Searching addresses near (%s, %s) radius=%s km",
        latitude, longitude, radius_km
    )

    rows = crud.list_addresses_nearby(
        db,
        latitude,
        longitude,
        radius_km,
        limit=limit,
        offset=offset
    )

    # Return only the address objects
    return [r["address"] for r in rows]
