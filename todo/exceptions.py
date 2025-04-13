class TodoError(Exception):
    """Base exception for todo app errors"""
    pass

class TaskNotFoundError(TodoError):
    """Raised when a task is not found"""
    pass

class InvalidTaskDataError(TodoError):
    """Raised when task data is invalid"""
    pass