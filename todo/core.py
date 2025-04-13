from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
import datetime

class TaskNotFoundError(Exception):
    """Custom exception raised when a task is not found."""
    pass

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TaskStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

@dataclass
class Task:
    id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.MEDIUM
    deadline: Optional[datetime.date] = None

class TodoList:
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1

    def add_task(self, title: str, priority: Priority = Priority.MEDIUM, deadline: Optional[datetime.date] = None) -> Task:
        """Add a new task to the todo list"""
        task = Task(id=self.next_id, title=title, priority=priority, deadline=deadline)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by its ID"""
        task = self._find_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        self.tasks.remove(task)

    def mark_completed(self, task_id: int) -> Task:
        """Mark a task as completed"""
        task = self._find_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        task.status = TaskStatus.COMPLETED
        return task

    def list_tasks(self, filter_status: Optional[TaskStatus] = None) -> List[Task]:
        """List all tasks, optionally filtered by status"""
        if filter_status:
            return [task for task in self.tasks if task.status == filter_status]
        return self.tasks.copy()

    def _find_task(self, task_id: int) -> Optional[Task]:
        """Internal method to find a task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None