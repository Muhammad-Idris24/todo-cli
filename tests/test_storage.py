import pytest
import json
from pathlib import Path
from datetime import date
from todo.core import Task, Priority, TaskStatus
from todo.storage import Storage

@pytest.fixture
def storage(tmp_path):
    return Storage(file_path=tmp_path / "test_tasks.json")

def test_save_and_load_tasks(storage):
    tasks = [
        Task(id=1, title="Task 1", status=TaskStatus.PENDING, priority=Priority.MEDIUM),
        Task(id=2, title="Task 2", status=TaskStatus.COMPLETED, priority=Priority.HIGH, 
             deadline=date(2023, 12, 31))
    ]
    
    storage.save_tasks(tasks)
    loaded_tasks = storage.load_tasks()
    
    assert len(loaded_tasks) == 2
    assert loaded_tasks[0].title == "Task 1"
    assert loaded_tasks[1].status == TaskStatus.COMPLETED
    assert loaded_tasks[1].deadline == date(2023, 12, 31)

def test_load_empty_file(storage):
    tasks = storage.load_tasks()
    assert tasks == []