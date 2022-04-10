import os
import pathlib
import subprocess

import sys

current_file_dir = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
sys.argv.extend(
    ["--cfg", str(current_file_dir.joinpath("cfg.yaml"))]
)  # passing cfg as it is passed from command line

from pydantic import BaseSettings
from starlette.testclient import TestClient
import pytest

from src.main import app
from src.config import config

test_db = config.database


class Settings(BaseSettings):
    superuser: str = "shop"

    @classmethod
    def customise_sources(
        cls,
        init_settings,
        env_settings,
        file_secret_settings,
    ):
        return (
            env_settings,
            init_settings,
            file_secret_settings,
        )


settings = Settings()


def create_test_database():
    commands = [
        f"DROP DATABASE IF EXISTS {test_db.name} WITH (FORCE)",
        f"DROP ROLE IF EXISTS {test_db.user}",
        f"CREATE USER {test_db.user} WITH PASSWORD '{test_db.password}'",
        f"CREATE DATABASE {test_db.name} WITH OWNER {test_db.user}",
    ]
    for cmd in commands:
        subprocess.check_output(["psql", "-U", settings.superuser, "-h", test_db.host, "-c", cmd])
    migration_cmd = [
        "flyway",
        f"-user={test_db.user}",
        f"-password={test_db.password}",
        "-sqlMigrationPrefix=v",
        f"-url=jdbc:postgresql://{test_db.host}:{test_db.port}/{test_db.name}",
        "-locations=filesystem:.",
        "migrate",
    ]
    migrations_path = current_file_dir.parents[2].joinpath("database/migrations")
    subprocess.run(migration_cmd, cwd=migrations_path, check=True)


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
