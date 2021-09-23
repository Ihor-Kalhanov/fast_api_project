from typing import Optional, List

from pydantic import PositiveInt

from apps import Base
from apps.cars.schemas import Car


class CatalogBase(Base):
    title: str


class CatalogCreate(CatalogBase):
    pass


class Catalog(CatalogBase):
    id: PositiveInt
    cars: Optional[List[Car]]


class Catalogs(Base):
    catalogs: List[Catalog]