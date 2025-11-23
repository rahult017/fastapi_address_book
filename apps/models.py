from sqlmodel import SQLModel, Field
from typing import Optional


class Address(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    street: str
    city: str
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: float
    longitude: float