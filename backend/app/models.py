from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, TIMESTAMP, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

"""
    SQLAlchemy ORM models for managing USERS
                                       TAGS 
                                       ASSIGNMENTS
                                       PROJECTS
                                       TASKS
    - additionally, many-to-many relationship between TASKS and TAGS managed via 'task_tags' table
    
"""


task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    assignments = relationship("Assignment", back_populates="user")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    title = Column(String(150), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="todo")
    due_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="tasks")
    assignments = relationship("Assignment", back_populates="task")
    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="assignments")
    task = relationship("Task", back_populates="assignments")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    color = Column(String(50), unique=True, nullable=False)

    tasks = relationship("Task", secondary=task_tags, back_populates="tags")
