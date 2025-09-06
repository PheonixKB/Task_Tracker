import os
import json
import argparse
from datetime import datetime
file_path="C:/VS_Code/Python/Repository/Task_Tracker/tasks.json"

def getNextID(tasks):
    if not tasks:
        return 1
    used_ids = {task['id'] for task in tasks}
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
    new_task={'id':getNextID(tasks),
              'description':task,
              'status':'todo',
              'created-at':now,
              'updated-at':now}
    tasks.append(new_task)
    with open(file_path,'w') as f:
        json.dump(tasks,f,indent=2)
    print(f"Task added successfully (ID:{new_task['id']})")

def lists(status=None):
    if not os.path.exists(file_path):
        print("Empty!")
        return
    with open(file_path,'r') as f:
        tasks=json.load(f)
    if status:
        tasks=[t for t in tasks if t['status']==status]
    if not tasks:
        print("No Task Found!")
        return
    print(f"{'ID':<5} | {'Description':<30} | {'Status':<12} | {'Created-At':<25} | {'Updated-At':<25}")
    print("-" * 105)
    for task in tasks:
        print(f"{task['id']:<5} | {task['description']:<30} | {task['status']:<12} | {task['created-at']:<25} | {task['updated-at']:<25}")

def mark(status,id):
    if not os.path.exists(file_path):
        print("Empty!")
    with open(file_path,'r') as f:
        tasks=json.load(f)
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for task in tasks:
        if task['id']==id:
            task['status']=status
            task['updated-at']=now
            print(f"ID:{task['id']} Status Updated.")
            break
    else:
        print(f"No task found with ID {id}.")
    with open(file_path,'w') as f:
        json.dump(tasks,f,indent=2)

def update(id,change):
    if not os.path.exists(file_path):
        print("Empty!")
        return
    with open(file_path,'r') as f:
        tasks=json.load(f)
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for task in tasks:
        if task['id']==id:
            task['description']=change
            task['updated-at']=now
            print(f"ID:{task['id']} Description Updated.")
            break
    else:
        print(f"No task found with ID {id}.")
    with open(file_path,'w') as f:
        json.dump(tasks,f,indent=2)

def delete(id):
    if not os.path.exists(file_path):
        print("Empty!")
        return
    with open(file_path,'r') as f:
        tasks=json.load(f)
    for i,task in enumerate(tasks):
        if task['id']==id:
            delete_task=tasks.pop(i)
            print(f"ID:{delete_task['id']} Deleted.")
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

#"mark" command
pMark=subparser.add_parser('mark',help='To update the status of the task.')
pMark.add_argument("status",help='Status of the Task.')
pMark.add_argument("id",type=int,help='ID of the Task.')

#"update" command
pUpdate=subparser.add_parser('update',help='Update the task.')
pUpdate.add_argument("id",type=int,help='ID of the task.')
pUpdate.add_argument("change",nargs=argparse.REMAINDER,help='Updation to make in the task.')

#"delete" command
pDelete=subparser.add_parser('delete',help='Delete the task.')
pDelete.add_argument("id",type=int,help='ID of the task.')

arg=parser.parse_args()

if arg.command=='add':
    add(arg.add)
elif arg.command=='list':
    lists(arg.status)
elif arg.command=='mark':
    mark(arg.status,arg.id)
elif arg.command=='update':
    update(arg.id," ".join(arg.change))
elif arg.command=='delete':
    delete(arg.id)