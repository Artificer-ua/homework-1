import asyncio
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from main import app
from src.database.connect import get_db
from src.entity.models import Base, Contact, User
from src.services.auth import auth_service

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)

test_user = {
    "username": "TestUser",
    "email": "testuser@example.com",
    "password": "12345678",
}
test_contact = {
    "firstname": "Name",
    "lastname": "LastName",
    "email": "lastname@example.com",
    "phone": "256789",
    "bday": datetime.strptime("1990-01-19", "%Y-%m-%d").date(),
    "notes": "",
}


@pytest.fixture(scope="module", autouse=True)
def init_models_wrap():
    async def init_models():
        async with engine.begin() as conn:
            # clear db
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async with TestingSessionLocal() as session:
            hash_password = auth_service.get_password_hash(test_user["password"])
            current_user = User(
                username=test_user["username"],
                email=test_user["email"],
                password=hash_password,
                avatar=None,
                confirmed=True,
            )
            session.add(current_user)
            await session.commit()
        async with TestingSessionLocal() as session:
            new_contact = Contact(
                firstname=test_contact["firstname"],
                lastname=test_contact["lastname"],
                email=test_contact["email"],
                phone=test_contact["phone"],
                bday=test_contact["bday"],
                notes=test_contact["notes"],
                user_id=1,
            )
            session.add(new_contact)
            await session.commit()

    asyncio.run(init_models())


# @pytest.fixture(scope="module")
# def session():
#     # Create the database
#
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@pytest.fixture(scope="module")
def client():
    # Dependency override
    async def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()

    # change client db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# generate user token fixture for every function
@pytest_asyncio.fixture()
async def get_token():
    token = await auth_service.create_access_token(data={"sub": test_user["email"]})
    return token
