import os
import pathlib

import sys

current_file_dir = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
sys.argv.extend(
    ["--cfg", str(current_file_dir.joinpath("cfg.yaml"))]
)  # passing cfg as it is passed from command line

from starlette.testclient import TestClient
import pytest

from src.main import app


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
