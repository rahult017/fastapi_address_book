from typing import Optional, List
from sqlmodel import select, Session

from .utils import haversine_distance
from .models import Address
from .schemas import AddressCreate,AddressUpdate


def create_address(db: Session, address_in: AddressCreate) -> Address:
    addr = Address.from_orm(address_in)
    db.add(addr)
    db.commit()
    db.refresh(addr)
    return addr


def get_address(db: Session, address_id: int) -> Optional[Address]:
    return db.get(Address, address_id)


def update_address(db: Session, address_id: int, address_in: AddressUpdate) -> Optional[Address]:
    addr = get_address(db, address_id)
    if not addr:
        return None

    updated_data = address_in.dict(exclude_unset=True)
    for key, val in updated_data.items():
        setattr(addr, key, val)

    db.add(addr)
    db.commit()
    db.refresh(addr)
    return addr


def delete_address(db: Session, address_id: int) -> bool:
    addr = get_address(db, address_id)
    if not addr:
        return False

    db.delete(addr)
    db.commit()
    return True


def list_addresses_nearby(
    db: Session,
    latitude: float,
    longitude: float,
    radius_km: float,
    limit: int = 100,
    offset: int = 0
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

    return [
        {"address": addr, "distance_km": dist}
        for addr, dist in nearby[:limit]
    ]
