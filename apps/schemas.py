import re

from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


class Coordinate(BaseModel):
    latitude: Decimal = Field(gt=-90, lt=90)
    longitude: Decimal = Field(gt=-180, lt=180)


class AddressCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    street: str = Field(min_length=1, max_length=200)
    city: str = Field(min_length=1, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    latitude: float
    longitude: float
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    building_number: Optional[str] = Field(
        None, max_length=50, description="Building number"
    )
    apartment: Optional[str] = Field(
        None, max_length=50, description="Apartment/suite number"
    )

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None

        # Basic postal code validation - can be customized per country
        if v is not None:
            if not re.match(r"^[A-Za-z0-9\s\-]+$", v):
                raise ValueError("Invalid postal code format")
            return v.strip()
        return v

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        if v < -90 or v > 90:
            raise ValueError("latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        if v < -180 or v > 180:
            raise ValueError("longitude must be between -180 and 180")
        return v


class AddressRead(AddressCreate):
    id: int


class AddressUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    street: Optional[str] = Field(None, min_length=1, max_length=200)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    building_number: Optional[str] = Field(
        None, max_length=50, description="Building number"
    )
    apartment: Optional[str] = Field(
        None, max_length=50, description="Apartment/suite number"
    )

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if v is not None:
            if not re.match(r"^[A-Za-z0-9\s\-]+$", v):
                raise ValueError("Invalid postal code format")
            return v.strip()
        return v

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: Optional[float]) -> Optional[float]:
        if v is None:
            return v
        if v < -90 or v > 90:
            raise ValueError("latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: Optional[float]) -> Optional[float]:
        if v is None:
            return v
        if v < -180 or v > 180:
            raise ValueError("longitude must be between -180 and 180")
        return v


class AddressSearchQuery(BaseModel):
    """Schema for address search query"""

    latitude: float = Field(..., ge=-90, le=90, description="Center point latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Center point longitude")
    distance_km: float = Field(
        ..., gt=0, le=10000, description="Search radius in kilometers"
    )
    limit: Optional[int] = Field(
        100, ge=1, le=1000, description="Maximum number of results"
    )


class AddressInDB(AddressCreate):
    """Schema for address stored in database"""

    id: int
    uuid: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class AddressResponse(BaseModel):
    id: int
    uuid: str
    name: Optional[str] = None  # ← key change
    street: str
    city: str
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: float
    longitude: float
    postal_code: Optional[str] = None
    building_number: Optional[str] = None
    apartment: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AddressSearchResult(BaseModel):
    """Schema for address search result"""

    address: AddressResponse
    distance_km: float = Field(
        ..., description="Distance from search center in kilometers"
    )

    class Config:
        from_attributes = True


class HealthCheck(BaseModel):
    """Health check response schema"""

    status: str
    version: str
    database: str
    timestamp: datetime
