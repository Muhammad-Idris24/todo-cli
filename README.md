# Todo CLI Application

A command-line todo list application with persistent storage.

## Features

- Add, list, complete, and delete tasks
- Set priorities (Low, Medium, High)
- Add deadlines to tasks
- Persistent storage in JSON format
- Colorful CLI output

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/todo-cli.git
cd todo-cli
```

2. Set up virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```
python -m todo.cli [command] [options]

Commands:
  add       Add a new task
  list      List tasks
  complete  Mark a task as completed
  delete    Delete a task

Options for 'add':
  -p, --priority  Priority level (1=Low, 2=Medium, 3=High)
  -d, --deadline  Deadline in YYYY-MM-DD format

Options for 'list':
  -s, --status    Filter by status (pending/completed)
```

### Examples

Add a task:
```bash
python -m todo.cli add "Buy groceries" -p 3 -d 2023-12-31
```

List all tasks:
```bash
python -m todo.cli list
```

List pending tasks:
```bash
python -m todo.cli list -s pending
```

Mark task as completed:
```bash
python -m todo.cli complete 1
```

Delete a task:
```bash
python -m todo.cli delete 2
```

## Future Improvements

- [ ] Add categories/tags for tasks
- [ ] Sync with Google Tasks API
- [ ] Add reminder functionality
- [ ] Implement task search
- [ ] Add export functionality (CSV, PDF)