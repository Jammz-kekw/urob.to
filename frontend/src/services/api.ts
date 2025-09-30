import axios from "axios";

/*
    API client for communicating with the FastAPI backend
    - exports interfaces to ease the endpoints
    - contains CRUD for the API calls
*/


const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export interface AssignmentPayload {
  id?: number;
  user: {
    id: number;
    username?: string;
    email?: string;
  };
}

export interface TagPayload {
  id: number;
  name?: string;
  color?: string;
}

export interface TaskPayload {
  id?: number;
  title: string;
  description?: string;
  status: "todo" | "in_progress" | "done";
  due_date?: string | null;
  project_id?: number;
  tags: number[]; 
  users: number[];
}

export interface ProjectPayload {
  id?: number;
  name: string;
  description: string;
  tasks: TaskPayload[]; 
}


// --- Projects ---
export const getProjects = () => api.get("/projects");
export const createProject = (data: {
  name: string;
  description: string;
  tasks?: any[];
  tags?: number[];
  users?: number[];
}) => api.post("/projects", data);
export const updateProject = (id: number, data: ProjectPayload) =>
  api.put(`/projects/${id}`, data);
export const deleteProject = (id: number) => api.delete(`/projects/${id}`);

// --- Tasks ---
export const getTasks = (projectId: number) =>
  api.get(`/projects/${projectId}`);
export const createTask = (data: {
  project_id: number;
  title: string;
  description?: string;
  status?: string;
}) => api.post("/tasks", data);
export const updateTask = (id: number, data: any) => api.put(`/tasks/${id}`, data);
export const deleteTask = (id: number) => api.delete(`/tasks/${id}`);

// --- Tags ---
export const getTags = () => api.get("/tags");

// --- Users ---
export const getUsers = () => api.get("/users");
