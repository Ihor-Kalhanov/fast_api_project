import uvicorn
from fastapi import Depends, FastAPI

from app import exceptions
from app.config import settings
from app.db.database import set_db
from app.apps.cars.views import car_router
from app.apps.catalog.views import catalog_router
from app.db.exceptions import DatabaseValidationError

from apps.accounts.views import user_router


def get_app() -> FastAPI:
    app = FastAPI(
        title=settings.SERVICE_NAME,
        debug=settings.DEBUG,
        dependencies=[Depends(set_db)],
    )

    app.include_router(car_router, prefix="/api", tags=['cars'])
    app.include_router(catalog_router, prefix="/api", tags=['catalogs'])
    app.include_router(user_router, prefix="/api", tags=['users'])

    app.add_exception_handler(
        DatabaseValidationError,
        exceptions.database_validation_exception_handler,
    )

    return app


app = get_app()

if __name__ == '__main__':
    uvicorn.run(
        'app.main:app',
        host='localhost',
        port=8000,
        reload=True,
        debug=True
    )
