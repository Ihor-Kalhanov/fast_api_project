from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import parse_obj_as

from app.apps.cars import schemas
from app.apps.cars import models
from app.db.utils import transaction

car_router = APIRouter()


@car_router.get("/catalog/{catalog_id}/cars/", response_model=schemas.Cars)
async def list_cars(catalog_id: int) -> schemas.Cars:
    objects = await models.Car.filter({"catalog_id": catalog_id})

    return schemas.Cars.parse_obj({"cars": objects})


@car_router.get("/catalog/{car_id}/", response_model=schemas.Car)
async def get_car(car_id: int) -> schemas.Car:
    instance = await models.Car.get_by_id(car_id)

    if not instance:
        raise HTTPException(status_code=404, detail="Card is not found")
    return schemas.Car.from_orm(instance)


@car_router.post("/catalog/{catalog_id}/cars/{user_id}/", response_model=schemas.Cars)
async def create_car(catalog_id: int, user_id: int, data: List[schemas.CarCreate]) -> schemas.Cars:
    async with transaction():
        objects = await models.Car.bulk_create(
            [models.Car(**car.dict(), catalog_id=catalog_id, user_id=user_id) for car in data],
        )
    return schemas.Cars.parse_obj({'cars': objects})


@car_router.put("/catalog/{catalog_id}/cars/{user_id}/", response_model=schemas.Cars)
async def update_car(catalog_id: int, data: List[schemas.Car]) -> schemas.Cars:
    async with transaction():
        objects = await models.Car.bulk_update(
            [models.Car(**card.dict(exclude={"catalog_id"}), deck_id=catalog_id) for card in data],
        )
    return schemas.Cars(items=parse_obj_as(List[schemas.Car], objects))
