from dataclasses import dataclass


@dataclass
class FarmDTO:
    name: str
    location: str
    municipality: str