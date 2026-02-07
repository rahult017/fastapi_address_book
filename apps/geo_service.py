from math import radians, sin, cos, sqrt, atan2
from typing import Tuple, List
from .logger import logger


class GeoService:
    """Service for geographical calculations"""

    # Earth's radius in kilometers
    EARTH_RADIUS_KM = 6371.0

    @staticmethod
    def calculate_distance(
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
    ) -> float:
        """
        Calculate the distance between two coordinates using Haversine formula
        """
        try:
            # Convert degrees to radians
            lat1_rad = radians(lat1)
            lon1_rad = radians(lon1)
            lat2_rad = radians(lat2)
            lon2_rad = radians(lon2)

            # Haversine formula
            dlat = lat2_rad - lat1_rad
            dlon = lon2_rad - lon1_rad

            a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = GeoService.EARTH_RADIUS_KM * c
            return round(distance, 4)  # Round to 4 decimal places (~10m precision)

        except Exception as e:
            logger.error(f"Error calculating distance: {e}")
            raise ValueError(f"Invalid coordinates: {e}")

    @staticmethod
    def validate_coordinates(
        latitude: float,
        longitude: float,
    ) -> bool:
        """Validate if coordinates are within valid ranges"""
        return -90 <= latitude <= 90 and -180 <= longitude <= 180

    @staticmethod
    def get_bounding_box(
        center_lat: float,
        center_lon: float,
        distance_km: float,
    ) -> Tuple[float, float, float, float]:
        """
        Calculate bounding box for efficient database queries
        """
        # Approximate degrees per kilometer at equator
        degrees_per_km = 1 / 111.0

        lat_delta = distance_km * degrees_per_km
        lon_delta = distance_km * degrees_per_km / abs(cos(radians(center_lat)))

        min_lat = center_lat - lat_delta
        max_lat = center_lat + lat_delta
        min_lon = center_lon - lon_delta
        max_lon = center_lon + lon_delta

        # Clamp to valid ranges
        min_lat = max(-90, min_lat)
        max_lat = min(90, max_lat)
        min_lon = max(-180, min_lon)
        max_lon = min(180, max_lon)

        return min_lat, max_lat, min_lon, max_lon
