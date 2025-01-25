from typing import Optional
from pydantic import BaseModel, Field

from faslava.core.utils import gettext_lazy as _


class LocationSerializer(BaseModel):
    lon: float = Field(description=_("Longitude"))
    lat: float = Field(description=_("Latitude"))


class GeoIPSerializer(BaseModel):
    ip: Optional[str] = Field(default=None, description=_("IPv4"))
    country_iso_code: Optional[str] = Field(
        default=None, description=_("Country code"), max_length=3, min_length=3
    )
    location: Optional[LocationSerializer] = Field(
        default=None, description=_("Location")
    )
    region_name: Optional[str] = Field(default=None, description=_("Region name"))
    continent_name: Optional[str] = Field(default=None, description=_("Continent name"))
    city_name: Optional[str] = Field(default=None, description=_("City name"))
