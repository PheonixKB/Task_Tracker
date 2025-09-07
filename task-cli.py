import os
import json
import argparse
from datetime import datetime
file_path="C:/VS_Code/Python/Repository/Task_Tracker/tasks.json"
archive_path='C:/VS_Code/Python/Repository/Task_Tracker/archive.json'
def getNextID():
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
    new_id = 1
    while new_id in used_ids:
        new_id += 1
    return new_id

def add(task):
    if not os.path.exists(file_path):
        with open(file_path,'w') as f:
            json.dump([],f)
    with open(file_path,'r') as f:
        tasks=json.load(f)
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_task={'id':getNextID(),
              'description':task,
              'status':'todo',
              'created-at':now,
              'updated-at':now}
    tasks.append(new_task)
    with open(file_path,'w') as f:
        json.dump(tasks,f,indent=2)
    print(f"Added Task (ID:{new_task['id']})")

def lists(status=None,sort=None,order=None,file="tasks"):
    if file=='archive':
        file=archive_path
    if not os.path.exists(file):
        print("Empty!")
        return
    with open(file,'r') as f:
        tasks=json.load(f)
    if status:
        tasks=[t for t in tasks if t['status']==status]
    if sort:
        reverse=(order=='desc')
        tasks.sort(key=lambda t:datetime.strptime(t[sort],"%Y-%m-%d %H:%M:%S"),reverse=reverse)
    if not tasks:
        print("No Task Found!")
        return
    header = f"{'ID':<5} | {'Description':<30} | {'Status':<12} | {'Created-At':<25} | {'Updated-At':<25}"
    if file == 'tasks':
        print(header)
        print("-" * len(header))
    else:
        header += f" | {'Archived-At':<25}"
        print(header)
        print("-" * len(header))

    for task in tasks:
        if file=='tasks':
            print(f"{task['id']:<5} | {task['description']:<30} | {task['status']:<12} | {task['created-at']:<25} | {task['updated-at']:<25}")
        else:
            print(f"{task['id']:<5} | {task['description']:<30} | {task['status']:<12} | {task['created-at']:<25} | {task['updated-at']:<25} | {task['archived-at']:<25}")
def modify(id,field,change):
    if not os.path.exists(file_path):
        print("File does not exists.")
        return
    if field=='description' and change=="":
        print("Description cannot be empty.")
        return
    with open(file_path,'r') as f:
        tasks=json.load(f)
  
    found=False
    valid_status=['todo','in-progress','done']
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for task in tasks:
        if task['id']==id:
            if field=='status' and change not in valid_status:
                print(f"Invalid status. Choose from {valid_status}")
                return
            task[field]=change
            task['updated-at']=now
            print(f"Updated Task ID:{id}")
            found=True
            break

    if not found:
        print(f"No task found with ID:{id}")

    with open(file_path,'w') as f:
        json.dump(tasks,f,indent=2)

def archive(criteria_list):
    # Join input into one string
    criteria_str = " ".join(criteria_list)

    # Standardize spacing around operators
    criteria_str = criteria_str.replace(" and ", " && ").replace(" or ", " || ")

    # Parse each simple condition into a tuple (field, [values])
    import re
    pattern = re.compile(r'(\w+)\s*=\s*([^&|]+)')
    matches = pattern.findall(criteria_str)
    if not matches:
        print("Invalid criteria format.")
        return

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

    # Convert criteria string to Python expression
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

    for task in tasks:
        try:
            if eval(expr.replace("&&", "and").replace("||", "or")):
                if not any(t['id'] == task['id'] for t in archive_tasks):
                    task['archived-at'] = now
                    archive_tasks.append(task)
                    count += 1
            else:
                remaining_tasks.append(task)
        except KeyError:
            remaining_tasks.append(task)  # ignore tasks missing some fields

    # Save back
    with open(file_path, 'w') as f:
        json.dump(remaining_tasks, f, indent=2)
    with open(archive_path, 'w') as f:
        json.dump(archive_tasks, f, indent=2)

    print(f"Archived {count} task(s) with criteria: {criteria_str}")

def delete(id):
    if not os.path.exists(file_path):
        print("Empty!")
        return
    with open(file_path,'r') as f:
        tasks=json.load(f)
    for i,task in enumerate(tasks):
        if task['id']==id:
            delete_task=tasks.pop(i)
            print(f"Deleted ID:{delete_task['id']}.")
            break
    else:
        print(f"No task found with ID {id}.")

    with open(file_path,'w') as f:
        json.dump(tasks,f,indent=2)

# -------------------- CLI --------------------
parser=argparse.ArgumentParser()
subparser=parser.add_subparsers(dest='command')

#"add" command
pAdd=subparser.add_parser('add',help='Adds a new task file.')
pAdd.add_argument("add",help='Description of the task.')

#"list" command
pLists=subparser.add_parser('list',help='List all the tasks.')
pLists.add_argument("status",nargs='?',choices=['todo','in-progress','done'],help="Status to find.")
pLists.add_argument("--sort",nargs="?",choices=['created-at','updated-at'],help="Sort by field.")
pLists.add_argument("--order",nargs="?",choices=['desc','asc'],default='asc',help="Sort order (default: asc).")
pLists.add_argument("--file",nargs="?",choices=['tasks','archive'],default='tasks',help="File to display (default: tasks).")

#"modify" command
pModify=subparser.add_parser('modify',help='Modify the tasks.')
pModify.add_argument('id',type=int,help='ID to modify.')
pModify.add_argument('field',choices=['description','status'],help='Field to be modify.')
pModify.add_argument('change',help='Change to be made.')

#"archive" command
pArchive=subparser.add_parser('archive',help='Archive the task in sepearate file.')
pArchive.add_argument('criteria',nargs='+',help='Criteria like field1=value1,value2... field2=value21,value22...')

#"delete" command
pDelete=subparser.add_parser('delete',help='Delete the task.')
pDelete.add_argument("id",type=int,help='ID of the task.')

arg=parser.parse_args()

if __name__=='__main__':
    if arg.command=='add':
        add(arg.add)
    elif arg.command=='list':
        lists(arg.status,arg.sort,arg.order,arg.file)
    elif arg.command=='modify':
        modify(arg.id,arg.field,arg.change)
    elif arg.command=='delete':
        delete(arg.id)
    elif arg.command=='archive':
        archive(arg.criteria)
