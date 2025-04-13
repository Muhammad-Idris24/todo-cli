from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import List, Optional   
from .core import Task
from enum import Enum
from datetime import datetime


class TaskStatus(Enum):
    COMPLETED = "completed"
    PENDING = "pending"

class GoogleTasksSync:
    def __init__(self, credentials: Credentials):
        self.service = build('tasks', 'v1', credentials=credentials)
    
    def get_tasks(self, tasklist_id: str = '@default') -> List[Task]:
        results = self.service.tasks().list(tasklist=tasklist_id).execute()
        return [
            Task(
                id=item['id'],
                title=item['title'],
                status=TaskStatus.COMPLETED if item.get('status') == 'completed' else TaskStatus.PENDING,
                deadline=datetime.fromisoformat(item['due']) if item.get('due') else None
            )
            for item in results.get('items', [])
        ]
    
    def add_task(self, task: Task, tasklist_id: str = '@default'):
        body = {
            'title': task.title,
            'due': task.deadline.isoformat() if task.deadline else None
        }
        return self.service.tasks().insert(tasklist=tasklist_id, body=body).execute()