from fastapi import APIRouter, HTTPException
from app.apps.accounts import schemas
from app.apps.accounts import models

user_router = APIRouter()


@user_router.get("/users/", response_model=schemas.Users)
async def list_users() -> schemas.Users:
    objects = await models.User.all(prefetch=('cars', ))
    return schemas.Users.parse_obj({'users': objects})


@user_router.get("/user/{user_id}/", response_model=schemas.User)
async def get_user(user_id: int) -> schemas.User:
    instance = await models.User.get_by_id(user_id, prefetch=("cars",))
    if not instance:
        raise HTTPException(status_code=404, detail='User is not fount')
    return schemas.User.from_orm(instance)


@user_router.post("/user/", response_model=schemas.User)
async def create_user(data: schemas.UserCreate) -> schemas.User:
    instance = models.User(**data.dict())

    await instance.save()
    return schemas.User.from_orm(instance)

