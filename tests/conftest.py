import pytest
from datetime import date
from bark.db_manager import DatabaseManager
from bark.persistence import BookmarkDatabase


def _create_table_name_with_date() -> str:
    return 'test_db_' + str(date.today()).replace('-', '_')


@pytest.fixture(scope="session")
def create_test_db() -> BookmarkDatabase:
    name_test_db = _create_table_name_with_date()
    db_class = DatabaseManager(f'{name_test_db}.db')
    db = BookmarkDatabase(table_name=name_test_db, db=db_class)
    yield db

    DatabaseManager.drop_table(db_class, table_name=name_test_db)
