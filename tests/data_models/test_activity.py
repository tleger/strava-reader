from typing import Generator

import pytest

from sqlmodel import create_engine, SQLModel
from sqlalchemy import Engine
from data_models.activity import Activity


@pytest.fixture(scope="function")
def setup_test_db(tmp_path) -> Generator[Engine, None, None]:
    """Fixture to set up and teardown the test database."""
    test_db_url = f"sqlite:///{tmp_path}/test_database.db"
    test_engine = create_engine(test_db_url, echo=False)
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    SQLModel.metadata.drop_all(test_engine)


def test_activity_model_initialization(setup_test_db: Engine):
    """Test initialization of the Activity model."""
    activity = Activity(
        name="Morning Run",
        distance=5000,
        moving_time=1800,
        elapsed_time=1900,
        total_elevation_gain=100,
        type="Run",
        id=1,
        start_date="2024-01-01T06:00:00Z",
        start_date_local="2024-01-01T06:00:00Z",
        timezone="GMT",
    )

    assert activity.name == "Morning Run"
    assert activity.distance == 5000
    assert activity.moving_time == 1800
    assert activity.elapsed_time == 1900
    assert activity.total_elevation_gain == 100
    assert activity.type == "Run"
    assert activity.id == 1
    assert activity.start_date == "2024-01-01T06:00:00Z"
    assert activity.start_date_local == "2024-01-01T06:00:00Z"
    assert activity.timezone == "GMT"


def test_activity_model_required_fields(setup_test_db: Engine):
    """Test required fields in the Activity model."""
    with pytest.raises(ValueError):
        # Try to create an Activity without required fields to ensure they are enforced
        _ = Activity(
            name="Morning Run",
            distance=5000,
            moving_time=1800,
            elapsed_time=1900,
            total_elevation_gain=100,
            type="Run",
            start_date="2024-01-01T06:00:00Z",
            start_date_local="2024-01-01T06:00:00Z",
            timezone="GMT",
        )
        # id is missing, which should raise a TypeError
