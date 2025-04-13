import pytest
from datetime import date
from todo.core import TodoList, Task, Priority, TaskStatus

@pytest.fixture
def todo():
    return TodoList()

def test_add_task(todo):
    task = todo.add_task("Test task")
    assert len(todo.list_tasks()) == 1
    assert task.title == "Test task"
    assert task.status == TaskStatus.PENDING
    assert task.priority == Priority.MEDIUM

def test_mark_completed(todo):
    task = todo.add_task("Test task")
    todo.mark_completed(task.id)
    assert task.status == TaskStatus.COMPLETED

def test_delete_task(todo):
    task = todo.add_task("Test task")
    todo.delete_task(task.id)
    assert len(todo.list_tasks()) == 0

def test_list_filtered_tasks(todo):
    task1 = todo.add_task("Task 1")
    task2 = todo.add_task("Task 2")
    todo.mark_completed(task1.id)
    
    pending_tasks = todo.list_tasks(filter_status=TaskStatus.PENDING)
    assert len(pending_tasks) == 1
    assert pending_tasks[0].id == task2.id
    
    completed_tasks = todo.list_tasks(filter_status=TaskStatus.COMPLETED)
    assert len(completed_tasks) == 1
    assert completed_tasks[0].id == task1.id