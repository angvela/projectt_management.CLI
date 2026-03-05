from datetime import datetime
from typing import List, Optional


class Task:
    def __init__(self, title: str, completed: bool = False, task_id: Optional[str] = None):
        self.id = task_id or str(datetime.now().timestamp())
        self.title = title
        self.completed = completed
        self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        task = cls(
            title=data["title"],
            completed=data.get("completed", False),
            task_id=data.get("id")
        )
        if "created_at" in data:
            task.created_at = datetime.fromisoformat(data["created_at"])
        return task
    
    def mark_complete(self):
        self.completed = True
    
    def __str__(self):
        status = "✅" if self.completed else "❌"
        return f"{self.title} [{status}]"


class Project:
    def __init__(self, title: str, owner: str, description: str = "", project_id: Optional[str] = None):
        self.id = project_id or str(datetime.now().timestamp())
        self.title = title
        self.owner = owner
        self.description = description
        self.tasks: List[Task] = []
        self.contributors: List[str] = []
        self.created_at = datetime.now()
    
    def add_task(self, task: Task):
        self.tasks.append(task)
    
    def remove_task(self, task_id: str) -> bool:
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                return True
        return False
    
    def get_task(self, task_id: str) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def add_contributor(self, username: str):
        if username not in self.contributors:
            self.contributors.append(username)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner,
            "description": self.description,
            "tasks": [task.to_dict() for task in self.tasks],
            "contributors": self.contributors,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        project = cls(
            title=data["title"],
            owner=data["owner"],
            description=data.get("description", ""),
            project_id=data.get("id")
        )
        project.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        project.contributors = data.get("contributors", [])
        if "created_at" in data:
            project.created_at = datetime.fromisoformat(data["created_at"])
        return project
    
    def __str__(self):
        task_count = len(self.tasks)
        completed_count = sum(1 for t in self.tasks if t.completed)
        return f"{self.title} ({completed_count}/{task_count} tasks)"


class User:
    def __init__(self, name: str, user_id: Optional[str] = None):
        self.id = user_id or str(datetime.now().timestamp())
        self.name = name
        self.projects: List[str] = []
        self.created_at = datetime.now()
    
    def add_project(self, project_id: str):
        if project_id not in self.projects:
            self.projects.append(project_id)
    
    def remove_project(self, project_id: str) -> bool:
        if project_id in self.projects:
            self.projects.remove(project_id)
            return True
        return False
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "projects": self.projects,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        user = cls(
            name=data["name"],
            user_id=data.get("id")
        )
        user.projects = data.get("projects", [])
        if "created_at" in data:
            user.created_at = datetime.fromisoformat(data["created_at"])
        return user
    
    def __str__(self):
        return self.name
