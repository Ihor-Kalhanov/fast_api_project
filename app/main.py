import uvicorn
from fastapi import Depends, FastAPI

from app import exceptions
from app.config import settings
from app.db.database import set_db
from app.apps.cars.views import car_router
from app.apps.catalog.views import catalog_router
from app.db.exceptions import DatabaseValidationError


def get_app() -> FastAPI:
    _app = FastAPI(
        title=settings.SERVICE_NAME,
        debug=settings.DEBUG,
        dependencies=[Depends(set_db)],
    )

    _app.include_router(car_router, prefix="/api", tags=['cars'])
    _app.include_router(catalog_router, prefix="/api", tags=['catalog'])

    _app.add_exception_handler(
        DatabaseValidationError,
        exceptions.database_validation_exception_handler,
    )

    return _app


app = get_app()


if __name__ == '__main__':
    uvicorn.run(
        'app.main:app',
        host='localhost',
        port=8000,
        reload=True,
        debug=True
    )

