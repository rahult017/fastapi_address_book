from typing import Optional
from uuid import uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import String, DateTime, func, Index
from sqlalchemy.dialects.postgresql import UUID
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Address(SQLModel, table=True):
    """Address model for SQLModel"""
    
    __tablename__ = "addresses"
    __table_args__ = (
        Index('idx_location', 'latitude', 'longitude'),
        Index('idx_city_country', 'city', 'country'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(
        default_factory=generate_uuid,
        sa_column=Column(String(36), unique=True, index=True)
    )
    name: Optional[str] = Field(default=None, max_length=150)
    street: str = Field(max_length=255, nullable=False)
    city: str = Field(max_length=100, nullable=False)
    state: str = Field(max_length=100, nullable=False)
    country: str = Field(max_length=100, nullable=False)
    postal_code: Optional[str] = Field(default=None,max_length=20,nullable=True)
    
    # Location coordinates (latitude, longitude)
    latitude: float = Field(nullable=False)
    longitude: float = Field(nullable=False)
    
    # Additional optional fields
    building_number: Optional[str] = Field(default=None, max_length=50, nullable=True)
    apartment: Optional[str] = Field(default=None, max_length=50, nullable=True)
    
    # Timestamps
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    
    def __repr__(self):
        return f"<Address {self.street}, {self.city}>"