import asyncio
import os
import subprocess

import sys

sys.argv.extend(
    ["--cfg", "integration/cfg.yaml"]
)  # passing cfg as it is passed from command line

from pydantic import BaseSettings
from starlette.testclient import TestClient
import pytest

from src.main import app
from src.config import config

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


@pytest.fixture
def client() -> TestClient:
    """
    New client per test case
    """
    with TestClient(
        app=app,
        base_url="http://test",
    ) as _client:
        yield _client
