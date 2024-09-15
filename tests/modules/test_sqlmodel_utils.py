import logging
from unittest.mock import patch, MagicMock, Mock

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import create_engine, SQLModel

from modules.sqlmodel_utils import save_activities_to_db

# Constants for test data
TEST_DB_URL = "sqlite:///test_database.db"
ACTIVITY_DATA = [
    {
        "name": "Morning Run",
        "distance": 5000,
        "moving_time": 1800,
        "elapsed_time": 1900,
        "total_elevation_gain": 100,
        "type": "Run",
        "id": 1,
        "start_date": "2024-01-01T06:00:00Z",
        "start_date_local": "2024-01-01T06:00:00Z",
        "timezone": "GMT",
    }
]


class TestSQLModelUtils:
    def setup_method(self):
        """Set up the test database."""
        self.test_engine = create_engine(TEST_DB_URL, echo=False)
        SQLModel.metadata.create_all(self.test_engine)

    def teardown_method(self):
        """Tear down the test database."""
        SQLModel.metadata.drop_all(self.test_engine)

    @patch("modules.sqlmodel_utils.Session")
    @pytest.mark.parametrize(
        "activities, expected_bulk_save_count, expected_commit_count, expected_rollback_count",
        [(ACTIVITY_DATA, 1, 1, 0), ([], 0, 0, 0)],
    )
    def test_save_activities_to_db(
        self,
        mock_session: Mock,
        activities: list,
        expected_bulk_save_count: int,
        expected_commit_count: int,
        expected_rollback_count: int,
    ):
        """Test saving activities to the database with different scenarios."""
        mock_session_instance = Mock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        save_activities_to_db(activities, db_engine=self.test_engine)

        assert (
            mock_session_instance.bulk_save_objects.call_count
            == expected_bulk_save_count
        )
        assert mock_session_instance.commit.call_count == expected_commit_count
        assert mock_session_instance.rollback.call_count == expected_rollback_count

    @patch("modules.sqlmodel_utils.Session")
    def test_save_activities_to_db_integrity_error(self, mock_session: Mock):
        """Test saving activities when an IntegrityError occurs."""
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session_instance.commit.side_effect = IntegrityError(
            "Mocked IntegrityError", None, Exception()
        )

        save_activities_to_db(ACTIVITY_DATA, db_engine=self.test_engine)

        assert mock_session_instance.bulk_save_objects.call_count == 1
        assert mock_session_instance.commit.call_count == 1
        assert mock_session_instance.rollback.call_count == 1

    @patch("modules.sqlmodel_utils.Session")
    def test_save_activities_to_db_logging(
        self, mock_session: Mock, caplog: pytest.LogCaptureFixture
    ):
        """Test logging during database operations."""
        mock_session_instance = Mock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        with caplog.at_level(logging.INFO):
            save_activities_to_db(ACTIVITY_DATA, db_engine=self.test_engine)
        assert "Successfully saved 1 records to the database." in caplog.text

        mock_session_instance.commit.side_effect = IntegrityError(
            "Mocked IntegrityError", None, Exception()
        )
        save_activities_to_db(ACTIVITY_DATA, db_engine=self.test_engine)
        assert (
            "Operation cancelled: Some records already exist in the database."
            in caplog.text
        )
