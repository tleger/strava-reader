from typing import Generator

import pytest

from sqlmodel import create_engine, SQLModel
from sqlalchemy import Engine
from data_models.route import Route


@pytest.fixture(scope="function")
def setup_test_db(tmp_path) -> Generator[Engine, None, None]:
    """Fixture to set up and teardown the test database."""
    test_db_url = f"sqlite:///{tmp_path}/test_database.db"
    test_engine = create_engine(test_db_url, echo=False)
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    SQLModel.metadata.drop_all(test_engine)


def test_route_model_initialization(setup_test_db: Engine):
    """Test initialization of the Route model."""
    route = Route(
        athlete_id=12345,
        description="Scenic route",
        distance=10000.0,
        elevation_gain=200.0,
        id=1,
        id_str="1",
        map_id="map1",
        map_polyline="polyline1",
        name="Morning Ride",
        private=False,
        resource_state=2,
        starred=False,
        sub_type=1,
        created_at="2024-01-01T06:00:00Z",
        updated_at="2024-01-01T06:00:00Z",
        timestamp=1672531200,
        type=1,
        estimated_moving_time=3600,
        waypoints="[]",
        segments="[]",
    )

    assert route.athlete_id == 12345
    assert route.description == "Scenic route"
    assert route.distance == 10000.0
    assert route.elevation_gain == 200.0
    assert route.id == 1
    assert route.id_str == "1"
    assert route.map_id == "map1"
    assert route.map_polyline == "polyline1"
    assert route.name == "Morning Ride"
    assert not route.private
    assert route.resource_state == 2
    assert not route.starred
    assert route.sub_type == 1
    assert route.created_at == "2024-01-01T06:00:00Z"
    assert route.updated_at == "2024-01-01T06:00:00Z"
    assert route.timestamp == 1672531200
    assert route.type == 1
    assert route.estimated_moving_time == 3600
    assert route.waypoints == "[]"
    assert route.segments == "[]"


def test_route_model_required_fields(setup_test_db: Engine):
    """Test required fields in the Route model."""
    with pytest.raises(ValueError):
        # Try to create a Route without required fields to ensure they are enforced
        _ = Route(
            athlete_id=12345,
            distance=10000.0,
            elevation_gain=200.0,
            id_str="1",
            map_id="map1",
            map_polyline="polyline1",
            name="Morning Ride",
            private=False,
            resource_state=2,
            starred=False,
            sub_type=1,
            created_at="2024-01-01T06:00:00Z",
            updated_at="2024-01-01T06:00:00Z",
            timestamp=1672531200,
            type=1,
            estimated_moving_time=3600,
            waypoints="[]",
            segments="[]",
        )
        # id is missing, which should raise a TypeError
