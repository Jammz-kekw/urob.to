import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// --- Projects ---
export const getProjects = () => api.get("/projects");
export const createProject = (data: { name: string; description: string }) =>
  api.post("/projects", data);
export const updateProject = (id: number, data: { name: string; description: string }) =>
  api.put(`/projects/${id}`, data);
export const deleteProject = (id: number) => api.delete(`/projects/${id}`);

// --- Tasks ---
export const getTasks = (projectId: number) =>
  api.get(`/projects/${projectId}`); // returns project incl. tasks
export const createTask = (data: {
  project_id: number;
  title: string;
  description?: string;
  status?: string;
}) => api.post("/tasks", data);
export const updateTask = (id: number, data: any) => api.put(`/tasks/${id}`, data);
export const deleteTask = (id: number) => api.delete(`/tasks/${id}`);
