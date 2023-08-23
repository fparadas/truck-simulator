from dataclasses import dataclass
from typing import List, Dict, Tuple, TypeAlias, Literal

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
Path: TypeAlias = Dict[Location]
Model: TypeAlias = Literal["car", "bus", "truck"]
Icon: TypeAlias = Literal["🚗", "🚌", "🚚"]
GeoLocation: TypeAlias = Tuple[float, float]
