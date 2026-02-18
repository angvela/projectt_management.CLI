import argparse
import json

DATA_FILE = "data/data.json"

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_user(name):
    data = load_data()
    

    for user in data["users"]:
        if user["name"] == name:
            print("User already exists.")
            return

    data["users"].append({"name": name, "projects": []})
    save_data(data)
    print("User added successfully!")

def list_users():
    data = load_data()
    for user in data["users"]:
        print("-", user["name"])
def add_project(user_name, title):
    data = load_data()

    
    for user in data["users"]:
        if user["name"] == user_name:
            
        
            user["projects"].append(title)

        
            data["projects"].append({
                "title": title,
                "owner": user_name,
                "tasks": []
            })

            save_data(data)
            print("Project added successfully!")
            return

    print("User not found.")
def add_task(project_title, task_title):
    data = load_data()


    for project in data["projects"]:
        if project["title"] == project_title:

            
            project["tasks"].append({
                "title": task_title,
                "completed": False
            })

            save_data(data)
            print("Task added successfully!")
            return

    print("Project not found.")
def complete_task(project_title, task_title):
    data = load_data()
    for project in data["projects"]:
        if project["title"] == project_title:
            for task in project["tasks"]:
                if task["title"] == task_title:
                    task["completed"] = True
                    save_data(data)
                    print(f"Task '{task_title}' marked as complete!")
                    return
            print("Task not found in this project.")
            return
    print("Project not found.")

def list_tasks(project_title):
    data = load_data()
    for project in data["projects"]:
        if project["title"] == project_title:
            if not project["tasks"]:
                print("No tasks for this project.")
                return
            print(f"Tasks for project '{project_title}':")
            for task in project["tasks"]:
                status = "✅" if task["completed"] else "❌"
                print(f"- {task['title']} [{status}]")
            return
    print("Project not found.")

def main():
    parser = argparse.ArgumentParser(description="Project CLI")
    subparsers = parser.add_subparsers(dest="command")

    
    add_user_parser = subparsers.add_parser("add-user")
    add_user_parser.add_argument("--name", required=True)

    
    subparsers.add_parser("list-users")
    add_project_parser = subparsers.add_parser("add-project")
    add_project_parser.add_argument("--user", required=True)
    add_project_parser.add_argument("--title", required=True)

    
    add_task_parser = subparsers.add_parser("add-task")
    add_task_parser.add_argument("--project", required=True)
    add_task_parser.add_argument("--title", required=True)


    complete_task_parser = subparsers.add_parser("complete-task")
    complete_task_parser.add_argument("--project", required=True)
    complete_task_parser.add_argument("--title", required=True)


    list_tasks_parser = subparsers.add_parser("list-tasks")
    list_tasks_parser.add_argument("--project", required=True)

 





    args = parser.parse_args()

    if args.command == "add-user":
        add_user(args.name)
    elif args.command == "list-users":
        list_users()
    elif args.command == "add-project":
        add_project(args.user, args.title)
    elif args.command == "add-task":
        add_task(args.project, args.title)
    elif args.command == "complete-task":
       complete_task(args.project, args.title)
    elif args.command == "list-tasks":
       list_tasks(args.project)



    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
#testing push

