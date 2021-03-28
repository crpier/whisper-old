import pytest
from unittest import mock
from typing import List

from beets.library import Item

from services.station import RadioQueue

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def setup_app():


@pytest.mark.functional
def test_create_station():
    response = client.post("/")
    print(response)
    assert response.status_code == 200
