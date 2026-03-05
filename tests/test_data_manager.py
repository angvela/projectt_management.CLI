import pytest
import os
import json
from data_manager import DataManager
from models import User, Project, Task


@pytest.fixture
def test_data_file(tmp_path):
    data_file = tmp_path / "test_data.json"
    return str(data_file)


@pytest.fixture
def data_manager(test_data_file):
    return DataManager(test_data_file)


class TestDataManager:
    def test_initialization(self, test_data_file):
        dm = DataManager(test_data_file)
        assert os.path.exists(test_data_file)
    
    def test_add_user(self, data_manager):
        user = User(name="TestUser")
        result = data_manager.add_user(user)
        
        assert result is True
        users = data_manager.get_all_users()
        assert len(users) == 1
        assert users[0].name == "TestUser"
    
    def test_add_duplicate_user(self, data_manager):
        user1 = User(name="TestUser")
        user2 = User(name="TestUser")
        
        result1 = data_manager.add_user(user1)
        result2 = data_manager.add_user(user2)
        
        assert result1 is True
        assert result2 is False
        users = data_manager.get_all_users()
        assert len(users) == 1
    
    def test_get_user_by_name(self, data_manager):
        user = User(name="TestUser")
        data_manager.add_user(user)
        
        found = data_manager.get_user_by_name("TestUser")
        assert found is not None
        assert found.name == "TestUser"
    
    def test_get_user_by_name_case_insensitive(self, data_manager):
        user = User(name="TestUser")
        data_manager.add_user(user)
        
        found = data_manager.get_user_by_name("testuser")
        assert found is not None
        assert found.name == "TestUser"
    
    def test_delete_user(self, data_manager):
        user = User(name="TestUser")
        data_manager.add_user(user)
        
        result = data_manager.delete_user("TestUser")
        assert result is True
        
        users = data_manager.get_all_users()
        assert len(users) == 0
    
    def test_add_project(self, data_manager):
        user = User(name="TestUser")
        data_manager.add_user(user)
        
        project = Project(title="TestProject", owner="TestUser")
        result = data_manager.add_project(project)
        
        assert result is True
        projects = data_manager.get_all_projects()
        assert len(projects) == 1
        assert projects[0].title == "TestProject"
    
    def test_add_project_without_user(self, data_manager):
        project = Project(title="TestProject", owner="NonExistentUser")
        result = data_manager.add_project(project)
        
        assert result is False
    
    def test_get_project_by_title(self, data_manager):
        user = User(name="TestUser")
        data_manager.add_user(user)
        
        project = Project(title="TestProject", owner="TestUser")
        data_manager.add_project(project)
        
        found = data_manager.get_project_by_title("TestProject")
        assert found is not None
        assert found.title == "TestProject"
    
    def test_get_projects_by_owner(self, data_manager):
        user = User(name="TestUser")
        data_manager.add_user(user)
        
        project1 = Project(title="Project1", owner="TestUser")
        project2 = Project(title="Project2", owner="TestUser")
        
        data_manager.add_project(project1)
        data_manager.add_project(project2)
        
        projects = data_manager.get_projects_by_owner("TestUser")
        assert len(projects) == 2
    
    def test_add_task_to_project(self, data_manager):
        user = User(name="TestUser")
        data_manager.add_user(user)
        
        project = Project(title="TestProject", owner="TestUser")
        data_manager.add_project(project)
        
        task = Task(title="TestTask")
        project.add_task(task)
        data_manager.update_project(project)
        
        updated_project = data_manager.get_project_by_title("TestProject")
        assert len(updated_project.tasks) == 1
        assert updated_project.tasks[0].title == "TestTask"
    
    def test_complete_task(self, data_manager):
        user = User(name="TestUser")
        data_manager.add_user(user)
        
        project = Project(title="TestProject", owner="TestUser")
        task = Task(title="TestTask")
        project.add_task(task)
        data_manager.add_project(project)
        
        project = data_manager.get_project_by_title("TestProject")
        project.tasks[0].mark_complete()
        data_manager.update_project(project)
        
        updated_project = data_manager.get_project_by_title("TestProject")
        assert updated_project.tasks[0].completed is True
    
    def test_search_projects(self, data_manager):
        user = User(name="TestUser")
        data_manager.add_user(user)
        
        project1 = Project(title="CLI Tool", owner="TestUser", description="A CLI tool")
        project2 = Project(title="Web App", owner="TestUser", description="A web application")
        
        data_manager.add_project(project1)
        data_manager.add_project(project2)
        
        results = data_manager.search_projects("CLI")
        assert len(results) == 1
        assert results[0].title == "CLI Tool"
    
    def test_search_tasks(self, data_manager):
        user = User(name="TestUser")
        data_manager.add_user(user)
        
        project = Project(title="TestProject", owner="TestUser")
        project.add_task(Task(title="Implement login"))
        project.add_task(Task(title="Implement logout"))
        
        data_manager.add_project(project)
        
        results = data_manager.search_tasks("login")
        assert len(results) == 1
        assert results[0][1].title == "Implement login"
    
    def test_delete_project(self, data_manager):
        user = User(name="TestUser")
        data_manager.add_user(user)
        
        project = Project(title="TestProject", owner="TestUser")
        data_manager.add_project(project)
        
        result = data_manager.delete_project("TestProject")
        assert result is True
        
        projects = data_manager.get_all_projects()
        assert len(projects) == 0
