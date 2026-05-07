from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities_state():
    baseline = deepcopy(app_module.activities)
    yield
    app_module.activities = deepcopy(baseline)
