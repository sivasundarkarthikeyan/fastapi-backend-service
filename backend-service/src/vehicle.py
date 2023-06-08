from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Vehicle(BaseModel):
    """Class with parameters similar to the DB table structure

    Args:
        BaseModel: inherits pydantic's BaseModel
    """
    id: Optional[int]
    brand: str
    description: str
    metadata: str
    year_of_manufacture: int
    ready_to_drive: bool
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    def sample_func_1(self):
        """Dummy function 1
        """

    def sample_func_2(self):
        """Dummy function 2
        """
