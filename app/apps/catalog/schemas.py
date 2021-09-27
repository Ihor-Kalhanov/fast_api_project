from typing import Optional, List

from pydantic import PositiveInt

from app.apps import Base
from app.apps.cars.schemas import Car, CarBase


class CatalogBase(Base):
    title: str


class CatalogCreate(CatalogBase):
    pass


class Catalog(CatalogBase):
    id: PositiveInt
    cars: Optional[List[Car]]


class Catalogs(Base):
    catalogs: Optional[List[Catalog]]
