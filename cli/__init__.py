import argparse
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None
    Table = None

from models import User, Project, Task
from data_manager import DataManager


if RICH_AVAILABLE:
    console = Console()
else:
    class SimpleConsole:
        def print(self, msg):
            print(msg)
    console = SimpleConsole()


class CLI:
    def __init__(self, data_file: str = "data/data.json"):
        self.data_manager = DataManager(data_file)
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Project Management CLI - Manage users, projects, and tasks",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s add-user --name "Alex"
  %(prog)s add-project --user "Alex" --title "CLI Tool"
  %(prog)s add-task --project "CLI Tool" --title "Implement add-task"
  %(prog)s list-projects --user "Alex"
  %(prog)s complete-task --project "CLI Tool" --title "Implement add-task"
            """
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        user_parser = subparsers.add_parser("add-user", help="Add a new user")
        user_parser.add_argument("--name", required=True, help="User's name")
        
        delete_user_parser = subparsers.add_parser("delete-user", help="Delete a user")
        delete_user_parser.add_argument("--name", required=True, help="User's name")
        
        subparsers.add_parser("list-users", help="List all users")
        
        project_parser = subparsers.add_parser("add-project", help="Add a new project")
        project_parser.add_argument("--user", required=True, help="Owner's username")
        project_parser.add_argument("--title", required=True, help="Project title")
        project_parser.add_argument("--description", default="", help="Project description")
        
        edit_project_parser = subparsers.add_parser("edit-project", help="Edit a project")
        edit_project_parser.add_argument("--title", required=True, help="Project title")
        edit_project_parser.add_argument("--description", help="New description")
        
        delete_project_parser = subparsers.add_parser("delete-project", help="Delete a project")
        delete_project_parser.add_argument("--title", required=True, help="Project title")
        
        list_projects_parser = subparsers.add_parser("list-projects", help="List all projects")
        list_projects_parser.add_argument("--user", help="Filter by owner")
        
        search_parser = subparsers.add_parser("search-projects", help="Search projects")
        search_parser.add_argument("--query", required=True, help="Search query")
        
        task_parser = subparsers.add_parser("add-task", help="Add a task to a project")
        task_parser.add_argument("--project", required=True, help="Project title")
        task_parser.add_argument("--title", required=True, help="Task title")
        
        complete_task_parser = subparsers.add_parser("complete-task", help="Mark a task as complete")
        complete_task_parser.add_argument("--project", required=True, help="Project title")
        complete_task_parser.add_argument("--title", required=True, help="Task title")
        
        list_tasks_parser = subparsers.add_parser("list-tasks", help="List tasks in a project")
        list_tasks_parser.add_argument("--project", required=True, help="Project title")
        
        search_tasks_parser = subparsers.add_parser("search-tasks", help="Search tasks")
        search_tasks_parser.add_argument("--query", required=True, help="Search query")
        
        subparsers.add_parser("info", help="Show system information")
        
        return parser
    
    def run(self, args: Optional[list] = None):
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.command:
            self.parser.print_help()
            return
        
        handlers = {
            "add-user": self.handle_add_user,
            "delete-user": self.handle_delete_user,
            "list-users": self.handle_list_users,
            "add-project": self.handle_add_project,
            "edit-project": self.handle_edit_project,
            "delete-project": self.handle_delete_project,
            "list-projects": self.handle_list_projects,
            "search-projects": self.handle_search_projects,
            "add-task": self.handle_add_task,
            "complete-task": self.handle_complete_task,
            "list-tasks": self.handle_list_tasks,
            "search-tasks": self.handle_search_tasks,
            "info": self.handle_info,
        }
        
        handler = handlers.get(parsed_args.command)
        if handler:
            handler(parsed_args)
    
    def _print(self, message: str, style: str = ""):
        if RICH_AVAILABLE:
            console.print(message)
        else:
            print(message)
    
    def _print_table(self, title: str, headers: list, rows: list):
        if RICH_AVAILABLE:
            table = Table(title=title, show_header=True, header_style="bold magenta")
            for header in headers:
                table.add_column(header)
            for row in rows:
                table.add_row(*row)
            console.print(table)
        else:
            print(f"\n=== {title} ===")
            print(" | ".join(headers))
            print("-" * 50)
            for row in rows:
                print(" | ".join(row))
            print()
    
    def handle_add_user(self, args):
        user = User(name=args.name)
        if self.data_manager.add_user(user):
            self._print(f"[green]✓[/green] User '{args.name}' added successfully!")
        else:
            self._print(f"[red]✗[/red] User '{args.name}' already exists.")
    
    def handle_delete_user(self, args):
        if self.data_manager.delete_user(args.name):
            self._print(f"[green]✓[/green] User '{args.name}' deleted successfully!")
        else:
            self._print(f"[red]✗[/red] User '{args.name}' not found.")
    
    def handle_list_users(self, args):
        users = self.data_manager.get_all_users()
        if not users:
            self._print("[yellow]No users found.[/yellow]")
            return
        
        rows = []
        for user in users:
            project_count = len(user.projects)
            rows.append([user.name, str(project_count)])
        
        self._print_table("Users", ["Name", "Projects"], rows)
    
    def handle_add_project(self, args):
        user = self.data_manager.get_user_by_name(args.user)
        if not user:
            self._print(f"[red]✗[/red] User '{args.user}' not found. Please create the user first.")
            return
        
        project = Project(title=args.title, owner=args.user, description=args.description)
        if self.data_manager.add_project(project):
            self._print(f"[green]✓[/green] Project '{args.title}' added successfully!")
        else:
            self._print(f"[red]✗[/red] Project '{args.title}' already exists.")
    
    def handle_edit_project(self, args):
        project = self.data_manager.get_project_by_title(args.title)
        if not project:
            self._print(f"[red]✗[/red] Project '{args.title}' not found.")
            return
        
        if args.description is not None:
            project.description = args.description
            self.data_manager.update_project(project)
            self._print(f"[green]✓[/green] Project '{args.title}' updated!")
        else:
            self._print("[yellow]No changes specified.[/yellow]")
    
    def handle_delete_project(self, args):
        if self.data_manager.delete_project(args.title):
            self._print(f"[green]✓[/green] Project '{args.title}' deleted successfully!")
        else:
            self._print(f"[red]✗[/red] Project '{args.title}' not found.")
    
    def handle_list_projects(self, args):
        if args.user:
            projects = self.data_manager.get_projects_by_owner(args.user)
        else:
            projects = self.data_manager.get_all_projects()
        
        if not projects:
            self._print("[yellow]No projects found.[/yellow]")
            return
        
        rows = []
        for project in projects:
            total_tasks = len(project.tasks)
            completed_tasks = sum(1 for t in project.tasks if t.completed)
            rows.append([
                project.title,
                project.owner,
                str(total_tasks),
                f"{completed_tasks}/{total_tasks}"
            ])
        
        title_suffix = f" - {args.user}'s" if args.user else ""
        self._print_table(f"Projects{title_suffix}", ["Title", "Owner", "Tasks", "Completed"], rows)
    
    def handle_search_projects(self, args):
        projects = self.data_manager.search_projects(args.query)
        
        if not projects:
            self._print(f"[yellow]No projects found matching '{args.query}'.[/yellow]")
            return
        
        rows = []
        for project in projects:
            rows.append([
                project.title,
                project.owner,
                project.description or "-"
            ])
        
        self._print_table(f"Search Results for '{args.query}'", ["Title", "Owner", "Description"], rows)
    
    def handle_add_task(self, args):
        project = self.data_manager.get_project_by_title(args.project)
        if not project:
            self._print(f"[red]✗[/red] Project '{args.project}' not found.")
            return
        
        task = Task(title=args.title)
        project.add_task(task)
        self.data_manager.update_project(project)
        self._print(f"[green]✓[/green] Task '{args.title}' added to project '{args.project}'!")
    
    def handle_complete_task(self, args):
        project = self.data_manager.get_project_by_title(args.project)
        if not project:
            self._print(f"[red]✗[/red] Project '{args.project}' not found.")
            return
        
        task_found = False
        for task in project.tasks:
            if task.title.lower() == args.title.lower():
                task.mark_complete()
                task_found = True
                break
        
        if task_found:
            self.data_manager.update_project(project)
            self._print(f"[green]✓[/green] Task '{args.title}' marked as complete!")
        else:
            self._print(f"[red]✗[/red] Task '{args.title}' not found in project '{args.project}'.")
    
    def handle_list_tasks(self, args):
        project = self.data_manager.get_project_by_title(args.project)
        if not project:
            self._print(f"[red]✗[/red] Project '{args.project}' not found.")
            return
        
        if not project.tasks:
            self._print("[yellow]No tasks in this project.[/yellow]")
            return
        
        rows = []
        for task in project.tasks:
            status = "✅" if task.completed else "❌"
            rows.append([task.title, status])
        
        self._print_table(f"Tasks in '{args.project}'", ["Task", "Status"], rows)
    
    def handle_search_tasks(self, args):
        results = self.data_manager.search_tasks(args.query)
        
        if not results:
            self._print(f"[yellow]No tasks found matching '{args.query}'.[/yellow]")
            return
        
        rows = []
        for project, task in results:
            status = "✅" if task.completed else "❌"
            rows.append([f"{task.title} [{status}]", project.title])
        
        self._print_table(f"Task Search Results for '{args.query}'", ["Task", "Project"], rows)
    
    def handle_info(self, args):
        users = self.data_manager.get_all_users()
        projects = self.data_manager.get_all_projects()
        total_tasks = sum(len(p.tasks) for p in projects)
        completed_tasks = sum(sum(1 for t in p.tasks if t.completed) for p in projects)
        
        rows = [
            ["Total Users", str(len(users))],
            ["Total Projects", str(len(projects))],
            ["Total Tasks", str(total_tasks)],
            ["Completed Tasks", f"{completed_tasks}/{total_tasks}"]
        ]
        
        self._print_table("System Information", ["Metric", "Value"], rows)


def main():
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
