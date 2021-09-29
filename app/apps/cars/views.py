from typing import List

import stripe
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
    breakpoint()
    if not instance:
        raise HTTPException(status_code=404, detail="Card is not found")
    return schemas.Car.from_orm(instance)


@car_router.post("/catalog/{catalog_id}/cars/", response_model=schemas.Cars)
async def create_car(catalog_id: int, user_id: int, data: List[schemas.CarCreate]) -> schemas.Cars:
    async with transaction():
        objects = await models.Car.bulk_create(
            [models.Car(**car.dict(), catalog_id=catalog_id, user_id=user_id) for car in data],
        )
    return schemas.Cars.parse_obj({'cars': objects})


@car_router.put("/catalog/{catalog_id}/cars/", response_model=schemas.Cars)
async def update_car(catalog_id: int, data: List[schemas.Car]) -> schemas.Cars:
    async with transaction():
        objects = await models.Car.bulk_update(
            [models.Car(**card.dict(exclude={"catalog_id"}), deck_id=catalog_id) for card in data],
        )
    return schemas.Cars(items=parse_obj_as(List[schemas.Car], objects))


@car_router.get('/buy/{car_id}/')
async def buy_car_by_user(car_id: int):
    stripe.api_key = 'sk_test_51JefdaKPKpDNZGt8OWUWbfrtketVGZuQBCdxG0erbRrYhI8qz3pBKFYFRtGk9xzt8vgZ2a95hXcMcQe1OhCKDcBW00sJlamRJ5'

    instance = await models.Car.get_by_id(car_id)

    product = stripe.Product.create(
        name='Starter pack of car'
    )
    price = stripe.Price.create(
        product=product,
        unit_amount=1000,
        currency='usd',
    )
    customer = stripe.Customer.create(
        email='test.test@example.com',
        payment_method='pm_card_visa',
        invoice_settings={
            'default_payment_method': 'pm_card_visa',
        },
    )
    subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[{
            'price_data': {
                'unit_amount': 5000,
                'currency': 'usd',
                'product': product,
                'recurring': {
                    'interval': 'month',
                },
            },
        }],
    )

    return subscription
