# Project Management CLI Tool

A command-line interface (CLI) application for managing users, projects, and tasks in a multi-user project tracking system.

## Features

- User Management: Create, list, and delete users
- Project Management: Create, edit, delete, and list projects with owner information
- Task Management: Add tasks to projects, mark tasks as complete, list and search tasks
- Search: Search projects and tasks by title or description
- Rich CLI Output: Beautiful formatted tables using the `rich` library
- Data Persistence: JSON-based local storage for all data
- Comprehensive Testing: Unit tests with pytest

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd project_management.CLI
```

2. Install the dependencies:
```bash
pip install -r requrements.txt
```

## Usage

### User Commands

```bash
python main.py add-user --name "Alex"
python main.py list-users
python main.py delete-user --name "Alex"
```

### Project Commands

```bash
python main.py add-project --user "Alex" --title "CLI Tool" --description "A project management CLI"
python main.py list-projects
python main.py list-projects --user "Alex"
python main.py edit-project --title "CLI Tool" --description "Updated description"
python main.py delete-project --title "CLI Tool"
python main.py search-projects --query "CLI"
```

### Task Commands

```bash
python main.py add-task --project "CLI Tool" --title "Implement add-task"
python main.py list-tasks --project "CLI Tool"
python main.py complete-task --project "CLI Tool" --title "Implement add-task"
python main.py search-tasks --query "add"
```

### Other Commands

```bash
python main.py info
python main.py --help
```

## Project Structure

```
project_management.CLI/
├── main.py
├── models/
│   └── __init__.py
├── data_manager/
│   └── __init__.py
├── cli/
│   └── __init__.py
├── tests/
├── data/
│   └── data.json
├── requrements.txt
└── README.md
```

## Running Tests

```bash
pytest
```

## Dependencies

- rich>=13.0.0
- pytest>=7.0.0
- pytest-cov>=4.0.0
