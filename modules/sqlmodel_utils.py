import logging

from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from sqlmodel import create_engine, Session, SQLModel

from data_models.activity import Activity

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


def save_activities_to_db(activities: list[dict], db_engine=engine) -> None:
    """Save the fetched activities to the SQLite database."""
    if len(activities) == 0:
        return
    with Session(db_engine) as session:
        activity_data = [
            Activity(
                name=activity["name"],
                distance=activity["distance"],
                moving_time=activity["moving_time"],
                elapsed_time=activity["elapsed_time"],
                total_elevation_gain=activity["total_elevation_gain"],
                type=activity["type"],
                id=activity["id"],
                start_date=activity["start_date"],
                start_date_local=activity["start_date_local"],
                timezone=activity["timezone"],
            )
            for activity in activities
        ]

        session.bulk_save_objects(activity_data)

        try:
            session.commit()
            logging.info(
                f"Successfully saved {len(activities)} activities to the database."
            )
        except IntegrityError:
            session.rollback()
            logging.warning(
                "Some activities already exist in the database and were skipped."
            )
