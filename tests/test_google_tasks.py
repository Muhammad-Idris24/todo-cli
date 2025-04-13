import pytest
from unittest.mock import Mock, patch
from datetime import date
from todo.google_tasks import GoogleTasksSync
from todo.core import Task, TaskStatus

@pytest.fixture
def mock_credentials():
    return Mock()

@pytest.fixture
def google_sync(mock_credentials):
    return GoogleTasksSync(mock_credentials)

def test_get_tasks(google_sync):
    # Mock API response
    mock_response = {
        'items': [
            {
                'id': 'task1',
                'title': 'Test Task 1',
                'status': 'needsAction',
                'due': '2023-12-31T00:00:00Z'
            },
            {
                'id': 'task2',
                'title': 'Test Task 2',
                'status': 'completed'
            }
        ]
    }
    
    # Patch the service mock
    with patch.object(google_sync.service.tasks(), 'list', 
                    return_value=mock_response) as mock_list:
        tasks = google_sync.get_tasks()
        
        # Assertions
        mock_list.assert_called_once_with(tasklist='@default')
        assert len(tasks) == 2
        assert tasks[0].id == 'task1'
        assert tasks[0].title == 'Test Task 1'
        assert tasks[0].status == TaskStatus.PENDING
        assert tasks[0].deadline == date(2023, 12, 31)
        assert tasks[1].status == TaskStatus.COMPLETED
        assert tasks[1].deadline is None

def test_get_tasks_empty(google_sync):
    with patch.object(google_sync.service.tasks(), 'list', 
                    return_value={}) as mock_list:
        tasks = google_sync.get_tasks()
        assert len(tasks) == 0

def test_add_task(google_sync):
    test_task = Task(
        id='new_task',
        title='New Task',
        status=TaskStatus.PENDING,
        deadline=date(2023, 12, 31)
    )
    
    mock_insert = Mock()
    google_sync.service.tasks.return_value = mock_insert
    
    with patch.object(mock_insert, 'insert') as mock_insert_call:
        google_sync.add_task(test_task)
        
        # Verify the call was made with correct parameters
        mock_insert_call.assert_called_once_with(
            tasklist='@default',
            body={
                'title': 'New Task',
                'due': '2023-12-31T00:00:00'
            }
        )

def test_add_task_no_deadline(google_sync):
    test_task = Task(
        id='new_task',
        title='New Task',
        status=TaskStatus.PENDING)
    
    mock_insert = Mock()
    google_sync.service.tasks.return_value = mock_insert
    
    with patch.object(mock_insert, 'insert') as mock_insert_call:
        google_sync.add_task(test_task)
        
        mock_insert_call.assert_called_once_with(
            tasklist='@default',
            body={
                'title': 'New Task',
                'due': None
            }
        )

def test_custom_tasklist(google_sync):
    with patch.object(google_sync.service.tasks(), 'list') as mock_list:
        google_sync.get_tasks(tasklist_id='custom_list')
        mock_list.assert_called_once_with(tasklist='custom_list')