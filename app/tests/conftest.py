import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.engine import Transaction
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.base import engine

from app.main import app


from app.db.database import session_context_var, set_db
from app.apps.cars import schemas as car_schemas, models as car_models
from app.apps.catalog import schemas as catalog_schemas, models as catalog_models


@pytest.fixture(scope="session")
def event_loop(request):
    """Redefined event loop fixture with bigger scope"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db():
    # https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    connection = await engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection, expire_on_commit=False, future=True)
    await connection.begin_nested()

    @event.listens_for(session.sync_session, "after_transaction_end")
    def end_savepoint(session: Session, transaction: Transaction) -> None:
        """async events are not implemented yet, recreates savepoints to avoid final commits"""
        # https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
        if connection.closed:
            return
        if not connection.in_nested_transaction():
            connection.sync_connection.begin_nested()

    yield session

    if session.in_transaction():
        await transaction.rollback()
    await connection.close()


@pytest.fixture
def db_context(db: AsyncSession):
    token = session_context_var.set(db)
    yield
    session_context_var.reset(token)


@pytest.fixture
def client(db_context):
    def _set_db() -> None:
        return None

    app.dependency_overrides[set_db] = _set_db
    with TestClient(app) as client:
        yield client


@pytest.fixture
async def catalog(db_context):
    catalog_data = catalog_schemas.CatalogCreate(
        **
        {
            "title": "test catalog title"
        }
    )
    catalog = catalog_models.Catalog(**catalog_data.dict())
    await catalog.save()
    return catalog

@pytest.fixture
async def car(db_context, catalog: catalog_models.Catalog):
    instance = car_models.Car(**car_data.dict(), catalog_id=catalog.id)
    await instance.save()
    return instance

car_data = car_schemas.CarCreate(
    name="test car name",
    description='test car description'
)
