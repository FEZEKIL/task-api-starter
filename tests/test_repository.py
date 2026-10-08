import os
import pytest
from app.repository import SQLiteTaskRepository

@pytest.fixture
def sqlite_repo(tmp_path):
    db_file = tmp_path / "test_tasks.db"
    os.environ["SQLITE_DB_PATH"] = str(db_file)
    repo = SQLiteTaskRepository()
    repo.init_db()
    yield repo
    if "SQLITE_DB_PATH" in os.environ:
        del os.environ["SQLITE_DB_PATH"]

def test_sqlite_repository_crud(sqlite_repo):
    # Initial seed check
    tasks = sqlite_repo.get_all()
    assert len(tasks) == 3

    # Create
    new_task = sqlite_repo.create("Test Task")
    assert new_task.id is not None
    assert new_task.title == "Test Task"
    assert new_task.done is False

    # Get by id
    fetched = sqlite_repo.get_by_id(new_task.id)
    assert fetched is not None
    assert fetched.title == "Test Task"

    # Search filter
    search_results = sqlite_repo.get_all(search="Test")
    assert len(search_results) == 1

    # Done filter
    done_results = sqlite_repo.get_all(done=True)
    assert len(done_results) == 1

    # Update
    updated = sqlite_repo.update(new_task.id, title="Updated Title", done=True)
    assert updated is not None
    assert updated.title == "Updated Title"
    assert updated.done is True

    # Stats
    stats = sqlite_repo.get_stats()
    assert stats["total"] == 4

    # Delete
    deleted = sqlite_repo.delete(new_task.id)
    assert deleted is True
    assert sqlite_repo.get_by_id(new_task.id) is None

    # Reset
    sqlite_repo.reset()
    assert len(sqlite_repo.get_all()) == 3
