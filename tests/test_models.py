import pytest
from models import User, Project, Task


class TestTask:
    def test_task_creation(self):
        task = Task(title="Test Task")
        assert task.title == "Test Task"
        assert task.completed is False
        assert task.id is not None
    
    def test_task_to_dict(self):
        task = Task(title="Test Task", task_id="task_001")
        task_dict = task.to_dict()
        
        assert task_dict["title"] == "Test Task"
        assert task_dict["completed"] is False
        assert task_dict["id"] == "task_001"
        assert "created_at" in task_dict
    
    def test_task_from_dict(self):
        data = {
            "id": "task_001",
            "title": "Test Task",
            "completed": True,
            "created_at": "2024-01-01T10:00:00"
        }
        task = Task.from_dict(data)
        
        assert task.id == "task_001"
        assert task.title == "Test Task"
        assert task.completed is True
    
    def test_mark_complete(self):
        task = Task(title="Test Task")
        assert task.completed is False
        
        task.mark_complete()
        assert task.completed is True


class TestProject:
    def test_project_creation(self):
        project = Project(title="Test Project", owner="Alex")
        assert project.title == "Test Project"
        assert project.owner == "Alex"
        assert project.description == ""
        assert project.tasks == []
        assert project.contributors == []
    
    def test_add_task(self):
        project = Project(title="Test Project", owner="Alex")
        task = Task(title="Test Task")
        
        project.add_task(task)
        assert len(project.tasks) == 1
        assert project.tasks[0] == task
    
    def test_remove_task(self):
        project = Project(title="Test Project", owner="Alex")
        task = Task(title="Test Task", task_id="task_001")
        project.add_task(task)
        
        result = project.remove_task("task_001")
        assert result is True
        assert len(project.tasks) == 0
    
    def test_get_task(self):
        project = Project(title="Test Project", owner="Alex")
        task = Task(title="Test Task", task_id="task_001")
        project.add_task(task)
        
        found_task = project.get_task("task_001")
        assert found_task is not None
        assert found_task.title == "Test Task"
    
    def test_add_contributor(self):
        project = Project(title="Test Project", owner="Alex")
        
        project.add_contributor("Bob")
        assert "Bob" in project.contributors
        
        project.add_contributor("Bob")
        assert project.contributors.count("Bob") == 1
    
    def test_project_to_dict(self):
        project = Project(title="Test Project", owner="Alex", description="A test project", project_id="proj_001")
        task = Task(title="Test Task", task_id="task_001")
        project.add_task(task)
        
        project_dict = project.to_dict()
        
        assert project_dict["title"] == "Test Project"
        assert project_dict["owner"] == "Alex"
        assert project_dict["description"] == "A test project"
        assert len(project_dict["tasks"]) == 1


class TestUser:
    def test_user_creation(self):
        user = User(name="Alex", user_id="user_001")
        assert user.name == "Alex"
        assert user.id == "user_001"
        assert user.projects == []
    
    def test_add_project(self):
        user = User(name="Alex")
        user.add_project("project_001")
        
        assert "project_001" in user.projects
        
        user.add_project("project_001")
        assert user.projects.count("project_001") == 1
    
    def test_remove_project(self):
        user = User(name="Alex")
        user.add_project("project_001")
        
        result = user.remove_project("project_001")
        assert result is True
        assert "project_001" not in user.projects
    
    def test_user_to_dict(self):
        user = User(name="Alex", user_id="user_001")
        user.add_project("project_001")
        
        user_dict = user.to_dict()
        
        assert user_dict["name"] == "Alex"
        assert user_dict["id"] == "user_001"
        assert "project_001" in user_dict["projects"]
