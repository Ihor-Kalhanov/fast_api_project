from typing import List

from fastapi import APIRouter, HTTPException
from apps.catalog import schemas
from apps.catalog import models

catalog_router = APIRouter()


@catalog_router.get("/catalog/", response_model=schemas.Catalogs)
async def list_catalog() -> schemas.Catalogs:
    objects = await models.Catalog.all()

    return schemas.Catalogs.parse_obj({'catalogs': objects})


@catalog_router.get("/catalog/{catalog_id}/", response_model=schemas.Catalog)
async def get_catalog(catalog_id: int) -> schemas.Catalog:
    instance = await models.Catalog.get_by_id(catalog_id)
    if not instance:
        raise HTTPException(status_code=404, detail='Catalog is not fount')
    return schemas.Catalog.from_orm(instance)


@catalog_router.put("/catalog/{catalog_id}/", response_model=schemas.Catalog)
async def update_catalog(catalog_id: int, data: schemas.CatalogCreate) -> schemas.Catalog:
    instance = await models.Catalog.get_by_id(catalog_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Catalog is not found")
    await instance.update_attrs(**data.dict())
    await instance.save()
    return schemas.Catalog.from_orm(instance)


@catalog_router.post("/catalog/", response_model=schemas.Catalog)
async def create_catalog(data: schemas.CatalogCreate) -> schemas.Catalog:
    instance = models.Catalog(**data.dict())
    try:
        await instance.save()
        return schemas.Catalog.from_orm(instance)
    except:
        raise HTTPException(status_code=409, detail="Catalog is already exist")
