import asyncio
import os
import subprocess

import pytest
import sys

sys.path.append("../src")
sys.argv.extend(["--cfg", "cfg.yaml"])

import sqlalchemy.orm
from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient


from main import app
from config import config

test_db = config.database


class Settings(BaseSettings):
    db_superuser: str = "postgres"
    db_superuser_password: str = "postgres"


settings = Settings()


pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def create_test_database():
    pgpass_loc = "/tmp/.pgpass"
    with open(pgpass_loc, "w") as f:
        os.chmod(pgpass_loc, 0o600)
        f.write(
            f"{test_db.host}"
            f":{test_db.port}"
            f":postgres"
            f":{settings.db_superuser}"
            f":{settings.db_superuser_password}"
        )
    psql = subprocess.Popen(
        ["psql", "-U", settings.db_superuser, "-h", test_db.host],
        shell=False,
        stdin=subprocess.PIPE,
        env={"PGPASSFILE": pgpass_loc},
    )
    cmd = f"""
        DROP DATABASE IF EXISTS {test_db.name} WITH (FORCE);
        DROP ROLE IF EXISTS {test_db.user};
        CREATE USER {test_db.user} WITH PASSWORD '{test_db.password}' SUPERUSER;
        CREATE DATABASE {test_db.name} WITH OWNER {test_db.user};
    """.encode()
    psql.communicate(cmd)
    assert psql.returncode == 0

    migration_cmd = [
        "flyway",
        f"-user={test_db.user}",
        f"-password={test_db.password}",
        "-sqlMigrationPrefix=v",
        f"-url=jdbc:postgresql://{test_db.host}:{test_db.port}/{test_db.name}",
        "-locations=filesystem:.",
        "migrate",
    ]
    subprocess.run(migration_cmd, cwd="../../database/migrations", check=True)


create_test_database()

engine = create_engine(
    f"postgresql+pg8000://{test_db.user}:{test_db.password}@{test_db.host}/{test_db.name}",
    pool_size=test_db.pool_size,
    max_overflow=5,
)
Session = sessionmaker(engine)


@pytest.fixture
def client() -> TestClient:
    """
    Authorized client
    """
    with TestClient(
        app=app,
        base_url="http://test",
    ) as _client:
        yield _client


@pytest.fixture
def test_data(client) -> list[dict]:
    products = [
        {"name": "melon", "price": 5},
        {"name": "orange", "price": 1.5},
        {"name": "bread", "price": 3},
        {"name": "watermelon", "price": 2},
        {"name": "milk", "price": 0.35},
    ]
    for product in products:
        client.put("/products", json=product)
    return products


@pytest.fixture
def db() -> sqlalchemy.orm.Session:
    session = Session()
    yield session
    session.commit()
    session.close()
