from pydantic import BaseModel, EmailStr
from typing import Optional, List

# --- Tags ---
class TagBase(BaseModel):
    name: str
    color: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    class Config:
        from_attributes = True

# --- Users ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

# --- Assignments ---
class AssignmentBase(BaseModel):
    user_id: int
    task_id: int

class AssignmentCreate(AssignmentBase):
    pass

# Here we embed the User for frontend convenience
class Assignment(BaseModel):
    id: int
    user: User

    class Config:
        from_attributes = True

# --- Tasks ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"
    due_date: Optional[str] = None

class TaskCreate(TaskBase):
    project_id: Optional[int] = None
    tags: List[int] = []           # Tag IDs
    users: List[int] = []          # User IDs

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[str] = None
    tags: Optional[List[int]] = None
    users: Optional[List[int]] = None

class Task(TaskBase):
    id: int
    project_id: int
    tags: List[Tag] = []
    assignments: List[Assignment] = []

    class Config:
        from_attributes = True

# --- Projects ---
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    tasks: List[TaskCreate] = []

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Project(ProjectBase):
    id: int
    tasks: List[Task] = []

    class Config:
        from_attributes = True
