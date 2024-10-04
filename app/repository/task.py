from sqlalchemy.orm import Session
from models.task import Task, TaskStatus
from schemas import TaskCreate, TaskUpdate  # Assuming you're using Pydantic schemas for validation
from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db  # Assuming you have a database dependency
from models.user import User
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
router = APIRouter()

# Create Task
@router.post('/tasks', tags=['Tasks'])
def create_task( request: TaskCreate, db: Session = Depends(get_db)):
    try:
        
        # Check if user_id exists in the User model
        user_exists = db.query(User).filter(User.id == request.user_id).first()
        if not user_exists:
            return JSONResponse({'status': 'error', 'error_code': 100, 'message': "User not found for this user ID."})

        # Check if the task already exists based on title or other criteria
        is_task_exist = db.query(Task).filter(Task.title == request.title).first()
        if not is_task_exist:
            # Process task creation
            new_task = Task(
                title=request.title,
                description=request.description,
                status=request.status or TaskStatus.TODO,
                priority=request.priority,
                due_date=request.due_date,
                user_id=request.user_id
            )
            db.add(new_task)
            db.commit()
            db.refresh(new_task)

            return JSONResponse({'status': 'success', 'error_code': 0, 'message': 'Task added successfully.'})
        else:
            return JSONResponse({'status': 'error', 'error_code': 100, 'message': 'Task with this title already exists.'})

    except NameError as e:
        return JSONResponse({'status': 'error', 'error_code': 103, 'message': f"Error: {e}"})
    except KeyError as e:
        return JSONResponse({'status': 'error', 'error_code': 102, 'message': f"Error: {e} is required"})
    except Exception as e:
        return JSONResponse({'status': 'error', 'error_code': 101, 'message': f"Error: {e}"})
# Read Task by ID
@router.get("/tasks/{task_id}", tags=['Tasks'])
def get_task_route(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    tasks= jsonable_encoder(db_task)
    if tasks:
        return JSONResponse({'status': 'success', 'error_code': 0, 'data': tasks})
    else:
        return JSONResponse({'status': 'error', 'error_code': 104, 'message': 'Task not found'})

# Read all Tasks for a User
@router.get("/tasks/", tags=['Tasks'])
def get_tasks_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user_id: int = 1):
    tasks = db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()
    count_tasks = len(tasks)
    if count_tasks > 0:
        task_data = jsonable_encoder(tasks)
        return JSONResponse({'status': 'success', 'error_code': 0, 'data': task_data})
    else:
        return JSONResponse({'status': 'error', 'error_code': 103, 'data': 'No tasks found'})
# Update Task
@router.put("/tasks/{task_id}", tags=['Tasks'])
def update_task_route(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if the new title already exists for another task
    if task_update.title:
        existing_task = db.query(Task).filter(Task.title == task_update.title, Task.id != task_id).first()
        if existing_task:
            return JSONResponse(
        content={
            'status': 'error',
            'error_code': 101,
            'message': 'A task with this title already exists.'}
            
    )
    # Update task fields only if they are provided
    db_task.title = task_update.title or db_task.title
    db_task.description = task_update.description or db_task.description
    db_task.status = task_update.status or db_task.status
    db_task.priority = task_update.priority or db_task.priority
    db.commit()
    db.refresh(db_task)
    
    return JSONResponse(
        content={
            'status': 'success',
            'error_code': 0,
            'message': 'Task updated successfully.',
            'data': jsonable_encoder(db_task)  # Ensure it is JSON serializable
        },
        status_code=200
    )
# Delete Task
@router.delete("/tasks/{task_id}",tags=['Tasks'])
def delete_task_route(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return JSONResponse(
    content={
        'status': 'success',
        'error_code': 0,
        'message': 'Task deleted successfully.',
        'data': jsonable_encoder(db_task)  # Ensure it is JSON serializable
    },
    status_code=200
)