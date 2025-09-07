import os
import json
import argparse
from datetime import datetime

# Paths to JSON files storing tasks and archived tasks
file_path = "C:/VS_Code/Python/Repository/Task_Tracker/tasks.json"
archive_path = 'C:/VS_Code/Python/Repository/Task_Tracker/archive.json'

# -------------------- Utility Functions --------------------

def getNextID():
    """
    Generate the next unique ID by checking both active and archived tasks.
    """
    used_ids = set()
    
    # Collect IDs from active tasks
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            tasks = json.load(f)
            used_ids.update(task['id'] for task in tasks)

    # Collect IDs from archived tasks
    if os.path.exists(archive_path):
        with open(archive_path, 'r') as f:
            archive_tasks = json.load(f)
            used_ids.update(task['id'] for task in archive_tasks)
    
    # Find the smallest unused ID
    new_id = 1
    while new_id in used_ids:
        new_id += 1
    return new_id

# -------------------- Task Operations --------------------

def add(task):
    """
    Add a new task with description 'task' to the active tasks list.
    """
    if not os.path.exists(file_path):
        with open(file_path,'w') as f:
            json.dump([],f)
    
    with open(file_path,'r') as f:
        tasks = json.load(f)
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_task = {
        'id': getNextID(),
        'description': task,
        'status': 'todo',
        'created-at': now,
        'updated-at': now
    }
    tasks.append(new_task)
    
    # Save back to file
    with open(file_path,'w') as f:
        json.dump(tasks,f,indent=2)
    
    print(f"Added Task (ID:{new_task['id']})")

def lists(status=None, sort=None, order=None, file="tasks"):
    """
    List tasks filtered by status, sorted by created/updated time.
    """
    if file == 'archive':
        file = archive_path
    if not os.path.exists(file):
        print("Empty!")
        return
    
    with open(file,'r') as f:
        tasks = json.load(f)
    
    # Filter by status if provided
    if status:
        tasks = [t for t in tasks if t['status'] == status]
    
    # Sort if requested
    if sort:
        reverse = (order == 'desc')
        tasks.sort(key=lambda t: datetime.strptime(t[sort], "%Y-%m-%d %H:%M:%S"), reverse=reverse)
    
    if not tasks:
        print("No Task Found!")
        return
    
    # Print header
    header = f"{'ID':<5} | {'Description':<30} | {'Status':<12} | {'Created-At':<25} | {'Updated-At':<25}"
    if file != archive_path:
        print(header)
        print("-" * len(header))
    else:
        header += f" | {'Archived-At':<25}"
        print(header)
        print("-" * len(header))
    
    # Print each task
    for task in tasks:
        if file != archive_path:
            print(f"{task['id']:<5} | {task['description']:<30} | {task['status']:<12} | {task['created-at']:<25} | {task['updated-at']:<25}")
        else:
            print(f"{task['id']:<5} | {task['description']:<30} | {task['status']:<12} | {task['created-at']:<25} | {task['updated-at']:<25} | {task['archived-at']:<25}")

def modify(id, field, change):
    """
    Modify the description or status of a task by its ID.
    """
    if not os.path.exists(file_path):
        print("File does not exist.")
        return
    
    if field == 'description' and change == "":
        print("Description cannot be empty.")
        return
    
    with open(file_path,'r') as f:
        tasks = json.load(f)
    
    found = False
    valid_status = ['todo','in-progress','done']
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for task in tasks:
        if task['id'] == id:
            if field == 'status' and change not in valid_status:
                print(f"Invalid status. Choose from {valid_status}")
                return
            task[field] = change
            task['updated-at'] = now
            print(f"Updated Task ID:{id}")
            found = True
            break
    
    if not found:
        print(f"No task found with ID:{id}")
    
    with open(file_path,'w') as f:
        json.dump(tasks,f,indent=2)

# -------------------- Archive Function --------------------

def archive(criteria_list):
    """
    Archive tasks based on complex criteria (multiple fields with AND/OR logic)
    Example input: ['id=1,2', 'status=todo,done', 'description=task1']
    Supports 'and' / 'or' between conditions.
    """
    # Combine criteria list into single string
    criteria_str = " ".join(criteria_list)
    
    # Standardize operators: 'and' -> '&&', 'or' -> '||'
    criteria_str = criteria_str.replace(" and ", " && ").replace(" or ", " || ")
    
    # Parse each simple condition using regex
    import re
    pattern = re.compile(r'(\w+)\s*=\s*([^&|]+)')
    matches = pattern.findall(criteria_str)
    if not matches:
        print("Invalid criteria format.")
        return
    
    # Convert parsed conditions to dictionary
    conditions = {}
    for field, values_str in matches:
        field = field.strip()
        values = [v.strip() for v in values_str.split(",")]
        if field == "id":
            try:
                values = [int(v) for v in values]
            except ValueError:
                print("IDs must be integers.")
                return
        conditions[field] = values
    
    # Build a Python expression to evaluate dynamically
    expr = criteria_str
    for field, values in conditions.items():
        if isinstance(values[0], int):
            val_str = " or ".join([f"task['{field}']=={v}" for v in values])
        else:
            val_str = " or ".join([f"task['{field}']=='{v}'" for v in values])
        expr = re.sub(rf'\b{field}\s*=\s*[^&|]+', f"({val_str})", expr)
    
    # Load tasks
    with open(file_path, 'r') as f:
        tasks = json.load(f)
    with open(archive_path, 'r') as f:
        archive_tasks = json.load(f)
    
    remaining_tasks = []
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    count = 0
    
    # Iterate through tasks and evaluate expression dynamically
    for task in tasks:
        try:
            # Replace '&&'/'||' with 'and'/'or' for Python syntax
            if eval(expr.replace("&&", "and").replace("||", "or")):
                # If task matches criteria and not already archived
                if not any(t['id'] == task['id'] for t in archive_tasks):
                    task['archived-at'] = now
                    archive_tasks.append(task)
                    count += 1
            else:
                remaining_tasks.append(task)
        except KeyError:
            # Ignore tasks that do not contain some fields
            remaining_tasks.append(task)
    
    # Save updated tasks and archive
    with open(file_path, 'w') as f:
        json.dump(remaining_tasks, f, indent=2)
    with open(archive_path, 'w') as f:
        json.dump(archive_tasks, f, indent=2)
    
    print(f"Archived {count} task(s) with criteria: {criteria_str}")

# -------------------- Delete Function --------------------

def delete(id):
    """
    Delete a task by ID from active tasks.
    """
    if not os.path.exists(file_path):
        print("Empty!")
        return
    
    with open(file_path,'r') as f:
        tasks = json.load(f)
    
    for i, task in enumerate(tasks):
        if task['id'] == id:
            delete_task = tasks.pop(i)
            print(f"Deleted ID:{delete_task['id']}.")
            break
    else:
        print(f"No task found with ID {id}.")
    
    # Save updated task list
    with open(file_path,'w') as f:
        json.dump(tasks,f,indent=2)

# -------------------- CLI Interface --------------------
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')

# "add" command
pAdd = subparser.add_parser('add', help='Adds a new task file.')
pAdd.add_argument("add", help='Description of the task.')

# "list" command
pLists = subparser.add_parser('list', help='List all the tasks.')
pLists.add_argument("status", nargs='?', choices=['todo','in-progress','done'], help="Status to find.")
pLists.add_argument("--sort", nargs="?", choices=['created-at','updated-at'], help="Sort by field.")
pLists.add_argument("--order", nargs="?", choices=['desc','asc'], default='asc', help="Sort order (default: asc).")
pLists.add_argument("--file", nargs="?", choices=['tasks','archive'], default='tasks', help="File to display (default: tasks).")

# "modify" command
pModify = subparser.add_parser('modify', help='Modify the tasks.')
pModify.add_argument('id', type=int, help='ID to modify.')
pModify.add_argument('field', choices=['description','status'], help='Field to be modified.')
pModify.add_argument('change', help='Change to be made.')

# "archive" command
pArchive = subparser.add_parser('archive', help='Archive the task in separate file.')
pArchive.add_argument('criteria', nargs='+', help='Criteria like field1=value1,value2... field2=value21,value22...')

# "delete" command
pDelete = subparser.add_parser('delete', help='Delete the task.')
pDelete.add_argument("id", type=int, help='ID of the task.')

arg = parser.parse_args()

# -------------------- CLI Execution --------------------
if __name__ == '__main__':
    if arg.command == 'add':
        add(arg.add)
    elif arg.command == 'list':
        lists(arg.status, arg.sort, arg.order, arg.file)
    elif arg.command == 'modify':
        modify(arg.id, arg.field, arg.change)
    elif arg.command == 'delete':
        delete(arg.id)
    elif arg.command == 'archive':
        archive(arg.criteria)
