from typing import AsyncGenerator
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.student.models import Base, College, Student
from src.main import app
import websockets
import json

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
def engine():
    return create_async_engine(DATABASE_URL, echo=True)

@pytest.fixture(scope="session")
async def setup_database(engine):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def async_session(setup_database, engine) -> AsyncGenerator[AsyncSession, None]:
    async_session_factory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session_factory() as session:
        yield session

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

@pytest.mark.asyncio
async def test_graphql_queries(async_session: AsyncSession, async_client: AsyncClient):
    async with async_session.begin():
        # Create some test data
        college = College(name="Test College", location="Test Location")
        async_session.add(college)
        await async_session.commit()

    # Test query
    query = """
    query {
      colleges {
        id
        name
        location
      }
    }
    """
    response = await async_client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "colleges" in data["data"]
    assert len(data["data"]["colleges"]) == 1

@pytest.mark.asyncio
async def test_graphql_mutations(async_client: AsyncClient):
    # Test mutation
    mutation = """
    mutation {
      create_college(name: "New College", location: "New Location") {
        id
        name
        location
      }
    }
    """
    response = await async_client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "create_college" in data["data"]
    assert data["data"]["create_college"]["name"] == "New College"
    assert data["data"]["create_college"]["location"] == "New Location"

@pytest.mark.asyncio
async def test_graphql_subscription():
    # Test subscription
    subscription = """
    subscription {
      studentAdded(collegeId: 1) {
        id
        name
        age
        collegeId
      }
    }
    """
    uri = "ws://localhost:8000/graphql"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"type": "connection_init"}))
        await websocket.send(json.dumps({"id": "1", "type": "start", "payload": {"query": subscription}}))
        response = await websocket.recv()
        response_data = json.loads(response)
        assert response_data["type"] == "data"
        assert "studentAdded" in response_data["payload"]["data"]
        assert response_data["payload"]["data"]["studentAdded"]["id"] is not None
