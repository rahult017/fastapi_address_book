from pydantic import BaseModel, condecimal, constr, validator
from typing import Optional


class Coordinate(BaseModel):
    latitude: condecimal(gt=-90, lt=90)
    longitude: condecimal(gt=-180, lt=180)


class AddressCreate(BaseModel):
    name: constr(min_length=1, max_length=150)
    street: constr(min_length=1, max_length=200)
    city: constr(min_length=1, max_length=100)
    state: Optional[constr(max_length=100)] = None
    country: Optional[constr(max_length=100)] = None
    latitude: float
    longitude: float

    @validator("latitude")
    def validate_latitude(cls, v):
        if v < -90 or v > 90:
            raise ValueError("latitude must be between -90 and 90")
        return v

    @validator("longitude")
    def validate_longitude(cls, v):
        if v < -180 or v > 180:
            raise ValueError("longitude must be between -180 and 180")
        return v


class AddressRead(AddressCreate):
    id: int


class AddressUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=150)] = None
    street: Optional[constr(min_length=1, max_length=200)] = None
    city: Optional[constr(min_length=1, max_length=100)] = None
    state: Optional[constr(max_length=100)] = None
    country: Optional[constr(max_length=100)] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @validator("latitude")
    def validate_latitude(cls, v):
        if v is None:
            return v
        if v < -90 or v > 90:
            raise ValueError("latitude must be between -90 and 90")
        return v

    @validator("longitude")
    def validate_longitude(cls, v):
        if v is None:
            return v
        if v < -180 or v > 180:
            raise ValueError("longitude must be between -180 and 180")
        return v
