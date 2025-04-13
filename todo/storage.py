import json
from datetime import datetime
from pathlib import Path
from typing import List
from .core import Task, Priority, TaskStatus

class Storage:
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = Path(file_path)

    def save_tasks(self, tasks: List[Task]) -> None:
        """Save tasks to JSON file"""
        serialized_tasks = []
        for task in tasks:
            serialized_task = {
                "id": task.id,
                "title": task.title,
                "status": task.status.value,
                "priority": task.priority.value,
                "deadline": task.deadline.isoformat() if task.deadline else None
            }
            serialized_tasks.append(serialized_task)

        with open(self.file_path, 'w') as f:
            json.dump(serialized_tasks, f, indent=2)

    def load_tasks(self) -> List[Task]:
        """Load tasks from JSON file"""
        if not self.file_path.exists():
            return []

        with open(self.file_path, 'r') as f:
            serialized_tasks = json.load(f)

        tasks = []
        for serialized_task in serialized_tasks:
            task = Task(
                id=serialized_task["id"],
                title=serialized_task["title"],
                status=TaskStatus(serialized_task["status"]),
                priority=Priority(serialized_task["priority"]),
                deadline=datetime.fromisoformat(serialized_task["deadline"]).date() if serialized_task["deadline"] else None
            )
            tasks.append(task)

        return tasks