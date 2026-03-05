import pytest
from cli import CLI
from data_manager import DataManager
from models import User, Project, Task


@pytest.fixture
def test_data_file(tmp_path):
    data_file = tmp_path / "test_data.json"
    return str(data_file)


@pytest.fixture
def cli(test_data_file):
    return CLI(test_data_file)


class TestCLI:
    def test_add_user_command(self, cli, capsys):
        cli.run(["add-user", "--name", "TestUser"])
        
        captured = capsys.readouterr()
        assert "TestUser" in captured.out
        assert "added successfully" in captured.out.lower()
        
        users = cli.data_manager.get_all_users()
        assert len(users) == 1
        assert users[0].name == "TestUser"
    
    def test_add_duplicate_user_command(self, cli, capsys):
        cli.run(["add-user", "--name", "TestUser"])
        cli.run(["add-user", "--name", "TestUser"])
        
        captured = capsys.readouterr()
        assert "already exists" in captured.out.lower()
    
    def test_list_users_command(self, cli, capsys):
        cli.data_manager.add_user(User(name="User1"))
        cli.data_manager.add_user(User(name="User2"))
        
        cli.run(["list-users"])
        
        captured = capsys.readouterr()
        assert "User1" in captured.out
        assert "User2" in captured.out
    
    def test_add_project_command(self, cli, capsys):
        cli.data_manager.add_user(User(name="TestUser"))
        
        cli.run(["add-project", "--user", "TestUser", "--title", "TestProject"])
        
        captured = capsys.readouterr()
        assert "TestProject" in captured.out
        assert "added successfully" in captured.out.lower()
    
    def test_add_project_without_user(self, cli, capsys):
        cli.run(["add-project", "--user", "NonExistent", "--title", "TestProject"])
        
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()
    
    def test_list_projects_command(self, cli, capsys):
        user = User(name="TestUser")
        cli.data_manager.add_user(user)
        
        project = Project(title="TestProject", owner="TestUser")
        cli.data_manager.add_project(project)
        
        cli.run(["list-projects"])
        
        captured = capsys.readouterr()
        assert "TestProject" in captured.out
        assert "TestUser" in captured.out
    
    def test_list_projects_by_user(self, cli, capsys):
        user1 = User(name="User1")
        user2 = User(name="User2")
        cli.data_manager.add_user(user1)
        cli.data_manager.add_user(user2)
        
        cli.data_manager.add_project(Project(title="Project1", owner="User1"))
        cli.data_manager.add_project(Project(title="Project2", owner="User2"))
        
        cli.run(["list-projects", "--user", "User1"])
        
        captured = capsys.readouterr()
        assert "Project1" in captured.out
        assert "Project2" not in captured.out
    
    def test_add_task_command(self, cli, capsys):
        user = User(name="TestUser")
        cli.data_manager.add_user(user)
        project = Project(title="TestProject", owner="TestUser")
        cli.data_manager.add_project(project)
        
        cli.run(["add-task", "--project", "TestProject", "--title", "TestTask"])
        
        captured = capsys.readouterr()
        assert "TestTask" in captured.out
        assert "added to" in captured.out.lower()
    
    def test_add_task_without_project(self, cli, capsys):
        cli.run(["add-task", "--project", "NonExistent", "--title", "TestTask"])
        
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()
    
    def test_list_tasks_command(self, cli, capsys):
        user = User(name="TestUser")
        cli.data_manager.add_user(user)
        project = Project(title="TestProject", owner="TestUser")
        project.add_task(Task(title="Task1"))
        project.add_task(Task(title="Task2"))
        cli.data_manager.add_project(project)
        
        cli.run(["list-tasks", "--project", "TestProject"])
        
        captured = capsys.readouterr()
        assert "Task1" in captured.out
        assert "Task2" in captured.out
    
    def test_complete_task_command(self, cli, capsys):
        user = User(name="TestUser")
        cli.data_manager.add_user(user)
        project = Project(title="TestProject", owner="TestUser")
        project.add_task(Task(title="Task1"))
        cli.data_manager.add_project(project)
        
        cli.run(["complete-task", "--project", "TestProject", "--title", "Task1"])
        
        captured = capsys.readouterr()
        assert "complete" in captured.out.lower()
        
        project = cli.data_manager.get_project_by_title("TestProject")
        assert project.tasks[0].completed is True
    
    def test_search_projects_command(self, cli, capsys):
        user = User(name="TestUser")
        cli.data_manager.add_user(user)
        project = Project(title="CLI Tool", owner="TestUser", description="A CLI tool")
        cli.data_manager.add_project(project)
        
        cli.run(["search-projects", "--query", "CLI"])
        
        captured = capsys.readouterr()
        assert "CLI Tool" in captured.out
    
    def test_search_tasks_command(self, cli, capsys):
        user = User(name="TestUser")
        cli.data_manager.add_user(user)
        project = Project(title="TestProject", owner="TestUser")
        project.add_task(Task(title="Implement login"))
        project.add_task(Task(title="Implement logout"))
        cli.data_manager.add_project(project)
        
        cli.run(["search-tasks", "--query", "login"])
        
        captured = capsys.readouterr()
        assert "login" in captured.out
        assert "logout" not in captured.out
    
    def test_info_command(self, cli, capsys):
        user = User(name="TestUser")
        cli.data_manager.add_user(user)
        project = Project(title="TestProject", owner="TestUser")
        project.add_task(Task(title="Task1"))
        cli.data_manager.add_project(project)
        
        cli.run(["info"])
        
        captured = capsys.readouterr()
        assert "Users" in captured.out
        assert "Projects" in captured.out
    
    def test_delete_user_command(self, cli, capsys):
        cli.data_manager.add_user(User(name="TestUser"))
        
        cli.run(["delete-user", "--name", "TestUser"])
        
        captured = capsys.readouterr()
        assert "deleted" in captured.out.lower()
        
        users = cli.data_manager.get_all_users()
        assert len(users) == 0
    
    def test_delete_project_command(self, cli, capsys):
        user = User(name="TestUser")
        cli.data_manager.add_user(user)
        project = Project(title="TestProject", owner="TestUser")
        cli.data_manager.add_project(project)
        
        cli.run(["delete-project", "--title", "TestProject"])
        
        captured = capsys.readouterr()
        assert "deleted" in captured.out.lower()
        
        projects = cli.data_manager.get_all_projects()
        assert len(projects) == 0
    
    def test_edit_project_command(self, cli, capsys):
        user = User(name="TestUser")
        cli.data_manager.add_user(user)
        project = Project(title="TestProject", owner="TestUser", description="Old description")
        cli.data_manager.add_project(project)
        
        cli.run(["edit-project", "--title", "TestProject", "--description", "New description"])
        
        captured = capsys.readouterr()
        assert "updated" in captured.out.lower()
        
        project = cli.data_manager.get_project_by_title("TestProject")
        assert project.description == "New description"
    
    def test_help_message(self, cli, capsys):
        cli.run([])
        
        captured = capsys.readouterr()
        assert "usage" in captured.out.lower() or "commands" in captured.out.lower()
