from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Vehicle(BaseModel):
    id: Optional[int]
    brand: str
    description: str
    metadata: str
    year_of_manufacture: int
    ready_to_drive: bool

    