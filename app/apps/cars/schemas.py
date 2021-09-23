from typing import List, Optional

from pydantic import PositiveInt

from apps import Base


class CarBase(Base):
    name: str
    description: Optional[str] = None


class CarCreate(CarBase):
    pass


class Car(CarBase):
    id: PositiveInt
    catalog_id: Optional[PositiveInt] = None


class Cars(Base):
    cars: List[Car]
