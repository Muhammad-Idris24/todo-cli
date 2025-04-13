import argparse
from datetime import datetime
from typing import List, Optional
from colorama import init, Fore, Style
from .core import TodoList, Task, Priority, TaskStatus
from .storage import Storage
from rich.console import Console
from rich.table import Table

init()  # Initialize colorama

class TodoCLI:
    def __init__(self):
        self.todo = TodoList()
        self.storage = Storage()
        self._load_tasks()
        
    def _load_tasks(self):
        """Load tasks from storage and update next_id"""
        tasks = self.storage.load_tasks()
        self.todo.tasks = tasks
        if tasks:
            self.todo.next_id = max(task.id for task in tasks) + 1

    def _save_tasks(self):
        """Save tasks to storage"""
        self.storage.save_tasks(self.todo.tasks)

    def run(self):
        """Parse command line arguments and execute appropriate command"""
        parser = argparse.ArgumentParser(description="A simple CLI Todo List App")
        subparsers = parser.add_subparsers(dest="command", required=True)

        # Add command
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("title", help="Title of the task")
        add_parser.add_argument("-p", "--priority", type=int, choices=[1, 2, 3],
                               default=2, help="Priority of task (1=Low, 2=Medium, 3=High)")
        add_parser.add_argument("-d", "--deadline", help="Deadline in YYYY-MM-DD format")

        # List command
        list_parser = subparsers.add_parser("list", help="List tasks")
        list_parser.add_argument("-s", "--status", choices=["pending", "completed"],
                                help="Filter tasks by status")

        # Complete command
        complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
        complete_parser.add_argument("task_id", type=int, help="ID of the task to complete")

        # Delete command
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")

        args = parser.parse_args()

        try:
            if args.command == "add":
                deadline = None
                if args.deadline:
                    deadline = datetime.strptime(args.deadline, "%Y-%m-%d").date()
                task = self.todo.add_task(
                    title=args.title,
                    priority=Priority(args.priority),
                    deadline=deadline
                )
                self._save_tasks()
                print(f"{Fore.GREEN}Task added successfully!{Style.RESET_ALL}")
                self._print_task(task)

            elif args.command == "list":
                status = TaskStatus(args.status.upper()) if args.status else None
                tasks = self.todo.list_tasks(filter_status=status)
                if not tasks:
                    print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
                else:
                    for task in tasks:
                        self._print_task(task)

            elif args.command == "complete":
                task = self.todo.mark_completed(args.task_id)
                self._save_tasks()
                print(f"{Fore.GREEN}Task marked as completed:{Style.RESET_ALL}")
                self._print_task(task)

            elif args.command == "delete":
                self.todo.delete_task(args.task_id)
                self._save_tasks()
                print(f"{Fore.GREEN}Task deleted successfully.{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def _print_task(self, task: Task):
        """Print a task with colored formatting"""
        status_color = Fore.GREEN if task.status == TaskStatus.COMPLETED else Fore.YELLOW
        priority_color = {
            Priority.LOW: Fore.BLUE,
            Priority.MEDIUM: Fore.YELLOW,
            Priority.HIGH: Fore.RED
        }[task.priority]

        deadline_str = f" | Deadline: {task.deadline}" if task.deadline else ""
        print(
            f"{Fore.CYAN}[{task.id}]{Style.RESET_ALL} {task.title} | "
            f"Status: {status_color}{task.status.value}{Style.RESET_ALL} | "
            f"Priority: {priority_color}{task.priority.name}{Style.RESET_ALL}"
            f"{deadline_str}"
        )
        
        def _print_tasks_table(self, tasks: List[Task]):
            """Print tasks in a rich table"""
            console = Console()
            table = Table(title="Todo List", show_header=True, header_style="bold magenta")
            
            table.add_column("ID", style="cyan")
            table.add_column("Title")
            table.add_column("Status")
            table.add_column("Priority")
            table.add_column("Deadline")
            
            for task in tasks:
                status_color = "green" if task.status == TaskStatus.COMPLETED else "yellow"
                priority_color = {
                    Priority.LOW: "blue",
                    Priority.MEDIUM: "yellow",
                    Priority.HIGH: "red"
                }[task.priority]
                
                deadline = task.deadline.strftime("%Y-%m-%d") if task.deadline else "None"
                
                table.add_row(
                    str(task.id),
                    task.title,
                    f"[{status_color}]{task.status.value}[/]",
                    f"[{priority_color}]{task.priority.name}[/]",
                    deadline
                )
    
            console.print(table)
        

if __name__ == "__main__":
    TodoCLI().run()