CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    project_id INT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'todo',
    due_date DATE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

INSERT INTO projects (name, description) VALUES
('Test Project', 'First project from init.sql');

INSERT INTO tasks (project_id, title, description, status) VALUES
(1, 'Set up backend', 'Run FastAPI in Docker', 'in_progress'),
(1, 'Create frontend', 'React app to connect API', 'todo');
