const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
console.log("API URL:", API_URL); 

export async function fetchProjects() {
  const res = await fetch(`${API_URL}/projects/`);
  if (!res.ok) throw new Error("Failed to fetch projects");
  return res.json();
}

export async function addProject(name: string) {
  const res = await fetch(`${API_URL}/projects/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) throw new Error("Failed to create project");
  return res.json();
}
