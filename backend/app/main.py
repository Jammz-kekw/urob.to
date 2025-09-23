from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, Base, get_db, SessionLocal
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ToDo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def seed_data():
    db: Session = SessionLocal()
    if not db.query(models.Tag).first():
        tag1 = models.Tag(name="Vysoká priorita", color="#F4320B")
        tag2 = models.Tag(name="Stredná priorita", color="#F58E27")
        tag3 = models.Tag(name="Nízka priorita", color="#F4DC0B")
        db.add_all([tag1, tag2, tag3])
        db.commit()
        db.refresh(tag1)
        db.refresh(tag2)
        db.refresh(tag3)

    if not db.query(models.User).first():
        user = models.User(username="John Doe", email="john.doe@mail.com")
        user1 = models.User(username="Jožko Ferko", email="jozok.ferko@mail.com")
        user2 = models.User(username="Palo Ščerba", email="palo.scerba@gmail.com")
        db.add_all([user, user1, user2])
        db.commit()
        db.refresh(user) 
        db.refresh(user1)
        db.refresh(user2)
    
    if not db.query(models.Project).first():
        project = models.Project(name="Testovací projekt", description="Projekt na demonštráciu funkcionalít aplikácie")
        db.add(project)
        db.commit()
        db.refresh(project)

        tags = db.query(models.Tag).all()
        users = db.query(models.User).all()

        tasks = [
            models.Task(project_id=project.id, 
                        title="Zriadenie backendu", 
                        description="Spustenie FastAPI prostredníctvom Dockeru", 
                        status="in_progress",
                        tags=[tags[1]],
                        assignments=[models.Assignment(user_id=users[0].id)]),
            
            models.Task(project_id=project.id,
                        title="Navrhnutie a napojenie frontendu", 
                        description="Napojenie Vue na API", 
                        status="todo",
                        tags=[tags[0]],
                        assignments=[
                            models.Assignment(user_id=users[1].id),
                            models.Assignment(user_id=users[2].id)
                        ])
        ]
        db.add_all(tasks)
        db.commit()

    db.close()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- Users ---
@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --- Tags ---
@app.post("/tags", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    return crud.create_tag(db, tag)

@app.get("/tags", response_model=list[schemas.Tag])
def read_tags(db: Session = Depends(get_db)):
    return crud.get_tags(db)

# --- Assignments ---
@app.post("/assignments", response_model=schemas.Assignment)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    return crud.create_assignment(db, assignment)

@app.get("/assignments", response_model=list[schemas.Assignment])
def read_assignments(db: Session = Depends(get_db)):
    return crud.get_assignments(db)

# --- Projects (CRUD) ---
@app.get("/projects", response_model=list[schemas.Project])
def read_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db)

@app.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.post("/projects", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, project)

@app.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    db_project = crud.update_project(db, project_id, project)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@app.delete("/projects/{project_id}", response_model=schemas.Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.delete_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

# --- Tasks (CRUD) ---
@app.get("/tasks", response_model=list[schemas.Task])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id, task)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
