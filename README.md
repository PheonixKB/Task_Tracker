# Task Tracker CLI

A Python command-line tool to **add, list, modify, delete, and archive tasks**.  
Tasks are stored in JSON files (`tasks.json` for active tasks, `archive.json` for archived tasks).

---

## Features

- Add tasks with a description.
- List tasks with optional filtering, sorting, and ordering.
- Modify tasks (status or description).
- Delete tasks by ID.
- Archive tasks using complex criteria (supporting `AND` / `OR` and multiple values).

---

## Setup

1. Make sure Python 3 is installed.
2. Clone or download this repository.
3. Run commands using:

```bash
python task_tracker.py <command> [options]
````

---

## Commands

### 1. Add a Task

Adds a new task to `tasks.json`.

```bash
python task_tracker.py add "Finish writing report"
```

Output:

```
Added Task (ID:1)
```

---

### 2. List Tasks

List tasks from `tasks.json` or `archive.json` with optional filters.

```bash
python task_tracker.py list
```

List all tasks.

```bash
python task_tracker.py list todo
```

List only tasks with status `todo`.

```bash
python task_tracker.py list --file archive
```

List tasks from the archive.

```bash
python task_tracker.py list --sort created-at --order desc
```

Sort by creation date in descending order.

---

### 3. Modify a Task

Modify task `status` or `description`.

```bash
python task_tracker.py modify 1 status done
```

Change task ID 1’s status to `done`.

```bash
python task_tracker.py modify 2 description "Fix bug in login page"
```

Change task ID 2’s description.

---

### 4. Delete a Task

Delete a task by its ID.

```bash
python task_tracker.py delete 1
```

Output:

```
Deleted ID:1.
```

---

### 5. Archive Tasks

Archive tasks based on criteria using **AND / OR logic**.

#### Examples:

* Archive tasks with status `todo` or `in-progress`:

```bash
python task_tracker.py archive "status=todo,in-progress"
```

* Archive tasks with ID 1 or 2 **AND** status `done`:

```bash
python task_tracker.py archive "id=1,2 and status=done"
```

* Archive tasks with description containing "Fix bug":

```bash
python task_tracker.py archive "description=Fix bug"
```

* Complex example using `OR`:

```bash
python task_tracker.py archive "status=todo or status=in-progress or id=5"
```

---

## Notes

* Task IDs are automatically generated and unique.
* JSON files are created automatically if missing.
* Archived tasks are moved to `archive.json` and removed from `tasks.json`.
* Fields supported in criteria: `id`, `status`, `description`.
* For multiple values in criteria, separate by commas.
* Use `and` / `or` for complex criteria.
* Tasks missing a field in the criteria are safely ignored during archive.

---

## File Structure

* `task_tracker.py` → Main Python CLI script.
* `tasks.json` → Active tasks.
* `archive.json` → Archived tasks.

---

## Example Workflow

1. Add tasks:

```bash
python task_tracker.py add "Finish project report"
python task_tracker.py add "Fix login bug"
```

2. List tasks:

```bash
python task_tracker.py list
```

3. Modify a task:

```bash
python task_tracker.py modify 2 status in-progress
```

4. Archive completed tasks:

```bash
python task_tracker.py archive "status=done"
```

5. Delete a task:

```bash
python task_tracker.py delete 1
```

6. View archived tasks:

```bash
python task_tracker.py list --file archive
```

---
