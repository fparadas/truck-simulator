from dataclasses import dataclass
from typing import Dict, TypeAlias, Literal

Location: TypeAlias = Literal[
    "AC",
    "AL",
    "AM",
    "AP",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MG",
    "MS",
    "MT",
    "PA",
    "PB",
    "PE",
    "PI",
    "PR",
    "RJ",
    "RN",
    "RO",
    "RR",
    "RS",
    "SC",
    "SE",
    "SP",
    "TO",
]
Path: TypeAlias = Dict[Location, Location]
Model: TypeAlias = Literal["car", "bus", "truck"]
Icon: TypeAlias = Literal["🚗", "🚌", "🚚"]

@dataclass
class GeoLocation:
    """
    A location on the map.

    Attributes:
        latitude (float): the latitude of the location.
        longitude (float): the longitude of the location.
    """

    latitude: float
    longitude: float