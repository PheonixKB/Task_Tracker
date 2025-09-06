# Task Tracker CLI

A command-line tool to manage tasks with features to add, list, update, mark, and delete tasks. Each task is stored in a JSON file with timestamps for creation and updates.

## Features

* Add new tasks with a description
* List all tasks or filter by status (`todo`, `in-progress`, `done`)
* Update the description of an existing task
* Mark tasks with a new status
* Delete tasks by ID
* Automatically maintains unique IDs
* Tracks timestamps for when a task was created and last updated

## Requirements

* Python 3.7 or higher
* No external dependencies (uses only Python standard library)

## Installation

1. Clone this repository or copy the source code into your local machine.
2. Ensure Python is installed and accessible in your system's PATH.
3. Save the script as `task-cli.py`.

## Usage

The script uses the `argparse` module to parse commands.

### 1. Add a Task

```bash
py task-cli.py add "Buy groceries"
```

Output:

```
Task added successfully (ID:1)
```

### 2. List Tasks

List all tasks:

```bash
py task-cli.py list
```

List tasks by status:

```bash
py task-cli.py list todo
py task-cli.py list in-progress
py task-cli.py list done
```

### 3. Mark Task Status

```bash
py task-cli.py mark done 1
```

Output:

```
ID:1 Status Updated.
```

### 4. Update Task Description

```bash
py task-cli.py update 1 "Buy groceries and cook dinner"
```

Output:

```
ID:1 Description Updated.
```

### 5. Delete Task

```bash
py task-cli.py delete 1
```

Output:

```
ID:1 Deleted.
```

## Data Storage

Tasks are stored in a JSON file located at:

```
C:/VS_Code/Python/Repository/Task_Tracker/tasks.json
```

Each task entry contains:

```json
{
  "id": 1,
  "description": "Buy groceries",
  "status": "todo",
  "created-at": "2025-09-05 23:55:20",
  "updated-at": "2025-09-05 23:55:20"
}
```

## Example Output

Command:

```bash
py task-cli.py list
```

Output:

```
ID    | Description                    | Status       | Created-At                | Updated-At
---------------------------------------------------------------------------------------------------------
1     | Buy groceries                  | todo         | 2025-09-05 23:55:20       | 2025-09-05 23:55:20
2     | Cook dinner                    | in-progress  | 2025-09-05 23:58:02       | 2025-09-05 23:59:12
```

---
