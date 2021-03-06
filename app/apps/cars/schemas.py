from typing import List, Optional

from pydantic import PositiveInt

from app.apps import Base



class CarBase(Base):
    name: str
    description: Optional[str] = None
    amount: Optional[int] = None



class CarCreate(CarBase):
    pass


class Car(CarBase):
    id: PositiveInt
    catalog_id: Optional[PositiveInt] = None
    user_id: Optional[PositiveInt] = None


class Cars(Base):
    cars: List[Car]
