from typing import Optional, List, Tuple
from sqlmodel import select, Session
from sqlalchemy import and_, or_

from .models import Address
from .schemas import AddressCreate, AddressUpdate, AddressSearchQuery
from .geo_service import GeoService

from .utils import haversine_distance

from .logger import logger


def create_address(
    db: Session,
    address_in: AddressCreate,
) -> Address:
    try:
        addr = Address.from_orm(address_in)
        db.add(addr)
        db.commit()
        db.refresh(addr)
        logger.info(f"Created address with ID {addr.id}")
        return addr
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating address: {e}")
        raise


def get_address(
    db: Session,
    address_id: int,
) -> Optional[Address]:
    try:
        return db.query(Address).filter(Address.id == address_id).first()
    except Exception as e:
        logger.error(f"Error getting address {address_id}: {e}")
        raise


def get_addresses(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> Tuple[List[Address], int]:
    try:
        query = db.query(Address)
        total = query.count()
        addresses = query.offset(skip).limit(limit).all()
        return addresses, total
    except Exception as e:
        logger.error(f"Error getting addresses: {e}")
        raise


def get_address_by_uuid(
    db: Session,
    address_uuid: str,
) -> Optional[Address]:
    """Get address by UUID"""
    try:
        return db.query(Address).filter(Address.uuid == address_uuid).first()
    except Exception as e:
        logger.error(f"Error getting address by UUID {address_uuid}: {e}")
        raise


def update_address(
    db: Session,
    address_id: int,
    address_in: AddressUpdate,
) -> Optional[Address]:
    try:
        addr = get_address(db, address_id)
        if not addr:
            return None

        updated_data = address_in.dict(exclude_unset=True)
        for key, val in updated_data.items():
            setattr(addr, key, val)

        db.add(addr)
        db.commit()
        db.refresh(addr)
        logger.info(f"Updated address with ID {addr.id}")
        return addr
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating address {addr.id}: {e}")
        raise


def delete_address(
    db: Session,
    address_id: int,
) -> bool:
    try:
        addr = get_address(db, address_id)
        if not addr:
            return False

        db.delete(addr)
        db.commit()
        logger.info(f"Deleted address with ID {address_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating address {addr.id}: {e}")
        raise


def list_addresses_nearby(
    db: Session,
    latitude: float,
    longitude: float,
    radius_km: float,
    limit: int = 100,
    offset: int = 0,
) -> List[dict]:
    # naive scan + Python-side haversine
    statement = (
        select(Address)
        .offset(offset)
        .limit(limit * 5)  # oversample for better filtering
    )
    results = db.exec(statement).all()

    nearby = []
    for addr in results:
        dist = haversine_distance(latitude, longitude, addr.latitude, addr.longitude)
        if dist <= radius_km:
            nearby.append((addr, dist))

    nearby.sort(key=lambda x: x[1])

    return [{"address": addr, "distance_km": dist} for addr, dist in nearby[:limit]]


def search_addresses_within_distance(
    db: Session,
    search_query: AddressSearchQuery,
) -> List[Tuple[Address, float]]:
    """Search addresses within a given distance from coordinates"""
    try:
        # Get bounding box for initial filtering
        min_lat, max_lat, min_lon, max_lon = GeoService.get_bounding_box(
            search_query.latitude, search_query.longitude, search_query.distance_km
        )

        # Initial query with bounding box filter
        query = db.query(Address).filter(
            and_(
                Address.latitude.between(min_lat, max_lat),
                Address.longitude.between(min_lon, max_lon),
            )
        )

        addresses = query.limit(search_query.limit * 2).all()  # Get extra for filtering

        # Calculate distances and filter
        results = []
        for address in addresses:
            distance = GeoService.calculate_distance(
                search_query.latitude,
                search_query.longitude,
                address.latitude,
                address.longitude,
            )

            if distance <= search_query.distance_km:
                results.append((address, distance))

        # Sort by distance and limit results
        results.sort(key=lambda x: x[1])
        return results[: search_query.limit]

    except Exception as e:
        logger.error(f"Error searching addresses: {e}")
