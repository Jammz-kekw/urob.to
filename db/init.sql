-- SQL script for initialization of PostgreSQL database 
-- creates new database with a new user and grants all priviliges
-- 
-- backend/app |- database.py - creates tables
--             |- schemas.py  - constais Pydantic schemas for data validation
--             |- main.py     - inserts default testing data into the database


CREATE DATABASE todo;

CREATE USER todo_user WITH ENCRYPTED PASSWORD 'todo_pass';

GRANT ALL PRIVILEGES ON DATABASE todo TO todo_user;
