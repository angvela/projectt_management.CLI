import json
import os
from typing import Optional
from models import User, Project, Task


class DataManager:
    def __init__(self, data_file: str = "data/data.json"):
        self.data_file = data_file
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            self._save_data({"users": [], "projects": []})
    
    def _load_data(self) -> dict:
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"users": [], "projects": []}
        except json.JSONDecodeError as e:
            print(f"Error loading data: {e}")
            return {"users": [], "projects": []}
    
    def _save_data(self, data: dict):
        try:
            with open(self.data_file, "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")
    
    def get_all_users(self) -> list[User]:
        data = self._load_data()
        return [User.from_dict(u) for u in data.get("users", [])]
    
    def get_user_by_name(self, name: str) -> Optional[User]:
        users = self.get_all_users()
        for user in users:
            if user.name.lower() == name.lower():
                return user
        return None
    
    def add_user(self, user: User) -> bool:
        data = self._load_data()
        
        for u in data["users"]:
            if u["name"].lower() == user.name.lower():
                return False
        
        data["users"].append(user.to_dict())
        self._save_data(data)
        return True
    
    def update_user(self, user: User):
        data = self._load_data()
        for i, u in enumerate(data["users"]):
            if u["id"] == user.id:
                data["users"][i] = user.to_dict()
                break
        self._save_data(data)
    
    def delete_user(self, name: str) -> bool:
        data = self._load_data()
        for i, u in enumerate(data["users"]):
            if u["name"].lower() == name.lower():
                data["users"].pop(i)
                data["projects"] = [p for p in data["projects"] if p["owner"].lower() != name.lower()]
                self._save_data(data)
                return True
        return False
    
    def get_all_projects(self) -> list[Project]:
        data = self._load_data()
        return [Project.from_dict(p) for p in data.get("projects", [])]
    
    def get_project_by_title(self, title: str) -> Optional[Project]:
        projects = self.get_all_projects()
        for project in projects:
            if project.title.lower() == title.lower():
                return project
        return None
    
    def get_projects_by_owner(self, owner: str) -> list[Project]:
        projects = self.get_all_projects()
        return [p for p in projects if p.owner.lower() == owner.lower()]
    
    def add_project(self, project: Project) -> bool:
        data = self._load_data()
        
        # Check if project already exists
        for p in data["projects"]:
            if p["title"].lower() == project.title.lower():
                return False
        
        # Check if user exists
        user_exists = False
        for u in data["users"]:
            if u["name"].lower() == project.owner.lower():
                user_exists = True
                break
        
        if not user_exists:
            return False
        
        data["projects"].append(project.to_dict())
        
        for u in data["users"]:
            if u["name"].lower() == project.owner.lower():
                if project.id not in u["projects"]:
                    u["projects"].append(project.id)
                break
        
        self._save_data(data)
        return True
    
    def update_project(self, project: Project):
        data = self._load_data()
        for i, p in enumerate(data["projects"]):
            if p["id"] == project.id:
                data["projects"][i] = project.to_dict()
                break
        self._save_data(data)
    
    def delete_project(self, title: str) -> bool:
        data = self._load_data()
        for i, p in enumerate(data["projects"]):
            if p["title"].lower() == title.lower():
                data["projects"].pop(i)
                for u in data["users"]:
                    if p["id"] in u["projects"]:
                        u["projects"].remove(p["id"])
                self._save_data(data)
                return True
        return False
    
    def search_projects(self, query: str) -> list[Project]:
        projects = self.get_all_projects()
        query_lower = query.lower()
        return [p for p in projects 
                if query_lower in p.title.lower() or query_lower in p.description.lower()]
    
    def search_tasks(self, query: str) -> list[tuple[Project, Task]]:
        results = []
        projects = self.get_all_projects()
        query_lower = query.lower()
        
        for project in projects:
            for task in project.tasks:
                if query_lower in task.title.lower():
                    results.append((project, task))
        
        return results
