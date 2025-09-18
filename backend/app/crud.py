from sqlalchemy.orm import Session
from . import models, schemas

# --- Users ---
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip=0, limit=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# --- Tags ---
def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def get_tags(db: Session):
    return db.query(models.Tag).all()

# --- Assignments ---
def create_assignment(db: Session, assignment: schemas.AssignmentCreate):
    db_assignment = models.Assignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def get_assignments(db: Session):
    return db.query(models.Assignment).all()

# --- Projects ---
def get_projects(db: Session, skip=0, limit=100):
    return db.query(models.Project).offset(skip).limit(limit).all()

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def create_project(db: Session, project: schemas.ProjectCreate):
    # Create base project
    db_project = models.Project(
        name=project.name,
        description=project.description
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    # --- Add tasks with tags and users ---
    for task_data in project.tasks:
        db_task = models.Task(
            project_id=db_project.id,
            title=task_data.title,
            description=task_data.description,
            status=task_data.status or "todo",
            due_date=task_data.due_date
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        # Attach tags
        if task_data.tags:
            tags = db.query(models.Tag).filter(models.Tag.id.in_(task_data.tags)).all()
            db_task.tags.extend(tags)

        # Attach users via assignments
        if task_data.users:
            users = db.query(models.User).filter(models.User.id.in_(task_data.users)).all()
            for user in users:
                assignment = models.Assignment(user_id=user.id, task_id=db_task.id)
                db.add(assignment)

        db.commit()

    db.refresh(db_project)
    return db_project



def update_project(db: Session, project_id: int, project: schemas.ProjectUpdate):
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    for key, value in project.dict(exclude_unset=True).items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project

# --- Tasks ---
def get_tasks(db: Session, skip=0, limit=100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
