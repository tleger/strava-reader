import logging
from typing import Type

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import create_engine, Session, SQLModel

from data_models.activity import Activity
from data_models.route import Route

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# load environment variables from .env file
load_dotenv(".env")

# Load database configuration from environment variables
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)
SQLModel.metadata.create_all(engine)


class DatabaseError(Exception):
    """Custom exception for database errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


def save_to_db(
    data: list[dict], model: Type[SQLModel], db_engine: Engine = engine
) -> None:
    """Generic function to save data to the SQLite database."""
    if not data:
        return

    with Session(db_engine) as session:
        model_data = [model(**item) for item in data]

        session.bulk_save_objects(model_data)

        try:
            session.commit()
            logging.info(f"Successfully saved {len(data)} records to the database.")
        except IntegrityError:
            session.rollback()
            logging.warning(
                "Operation cancelled: Some records already exist in the database."
            )
        except Exception as e:
            session.rollback()
            raise DatabaseError(f"Failed to save records to the database: {e}")


def save_activities_to_db(activities: list[dict], db_engine=engine) -> None:
    """Save the fetched activities to the SQLite database."""
    activity_data = [
        {
            "name": activity["name"],
            "distance": activity["distance"],
            "moving_time": activity["moving_time"],
            "elapsed_time": activity["elapsed_time"],
            "total_elevation_gain": activity["total_elevation_gain"],
            "type": activity["type"],
            "id": activity["id"],
            "start_date": activity["start_date"],
            "start_date_local": activity["start_date_local"],
            "timezone": activity["timezone"],
        }
        for activity in activities
    ]
    save_to_db(activity_data, Activity, db_engine)


def save_routes_to_db(routes: list[dict], db_engine=engine) -> None:
    """Save the fetched routes to the SQLite database."""
    route_data = [
        {
            "athlete_id": route["athlete"]["id"],
            "description": route.get("description", "No description available"),
            "distance": route["distance"],
            "elevation_gain": route["elevation_gain"],
            "id": route["id"],
            "id_str": route["id_str"],
            "map_id": route["map"]["id"],
            "map_polyline": route["map"].get("polyline", ""),
            "name": route["name"],
            "private": route["private"],
            "resource_state": route["resource_state"],
            "starred": route["starred"],
            "sub_type": route["sub_type"],
            "created_at": route["created_at"],
            "updated_at": route["updated_at"],
            "timestamp": route["timestamp"],
            "type": route["type"],
            "estimated_moving_time": route["estimated_moving_time"],
            "waypoints": str(route["waypoints"]),
            "segments": str(route["segments"]),
        }
        for route in routes
    ]
    save_to_db(route_data, Route, db_engine)
