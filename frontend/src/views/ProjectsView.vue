<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getProjects, deleteProject, createProject, updateProject, updateTask, getTags, getUsers } from "../services/api";
import type { ProjectPayload } from "../services/api";

/*
  Main ProjectsView displays PROJECTS with their asociated TASKS, TAGS and USERS
    - Allows users to:
      • View project details and task assignments
      • Add new projects with multiple tasks
      • Edit existing projects and tasks
      • Delete projects
      • Toggle task status (todo ↔ done)
    - Uses modals for add and update operations.
    - Data is fetched from backend services via `api.ts`.
*/

const projects = ref<any[]>([]);
const tags = ref<any[]>([]);
const users = ref<any[]>([]);
const showAddModal = ref(false); 
const showUpdateModal = ref(false);
const selectedProject = ref<any>(null);

const newProject = ref({
  name: "",
  description: "",
  tasks: [] as {
    title: string;
    description: string;
    status?: string;
    tags?: number[];
    users?: number[]; 
  }[],
});

const openUpdateModal = (project: any) => {
  selectedProject.value = {
    ...project,
    tasks: project.tasks.map((t: any) => ({
      ...t,
      tags: t.tags.map((tag: any) => tag.id),              
      users: t.assignments.map((a: any) => a.user.id)      
    }))
  };
  showUpdateModal.value = true;
};

const closeUpdateModal = () => {
  showUpdateModal.value = false;
  selectedProject.value = null;
};

const addTaskToUpdate = () => {
  selectedProject.value.tasks.push({
    title: "",
    description: "",
    status: "todo",
    tags: [],
    users: []
  });
};

const removeTaskFromUpdate = (index: number) => {
  selectedProject.value.tasks.splice(index, 1);
};

const saveProjectUpdate = async () => {
  if (!selectedProject.value) return;

  const payload: ProjectPayload = {
    id: selectedProject.value.id,
    name: selectedProject.value.name,
    description: selectedProject.value.description,
    tasks: selectedProject.value.tasks.map((task: any) => ({
      id: task.id,
      title: task.title,
      description: task.description,
      status: task.status,
      due_date: task.due_date || null,
      project_id: selectedProject.value.id,
      tags: task.tags,  
      users: task.users 
    }))
  };

  try {
    const res = await updateProject(selectedProject.value.id, payload);

    const index = projects.value.findIndex((p) => p.id === selectedProject.value.id);
    if (index !== -1) {
      projects.value[index] = res.data;
    }

    closeUpdateModal();
  } catch (err) {
    console.error("Failed to update project:", err);
    alert("Failed to update project");
  }
};

const loadProjects = async () => {
  try {
    const res = await getProjects();
    projects.value = res.data;
  } catch (err) {
    console.error("Failed to load projects:", err);
  }
};

const loadTagsAndUsers = async () => {
  try {
    const [tagsRes, usersRes] = await Promise.all([getTags(), getUsers()]);
    tags.value = tagsRes.data;
    users.value = usersRes.data;
  } catch (err) {
    console.error("Failed to load tags/users:", err);
  }
};

const removeProject = async (id: number) => {
  try {
    await deleteProject(id);
    projects.value = projects.value.filter((p) => p.id !== id);
  } catch (err) {
    console.error("Failed to delete project:", err);
  }
};

const addProject = async () => {
  try {
    const filteredTasks = newProject.value.tasks
      .filter(t => t.title.trim() !== "")
      .map(task => ({
        title: task.title,
        description: task.description || "",
        status: task.status || "todo",
        tags: task.tags || [],  
        users: task.users || [] 
      }));

    const payload = {
      name: newProject.value.name,
      description: newProject.value.description,
      tasks: filteredTasks
    };

    const res = await createProject(payload);

    projects.value.push(res.data);

    showAddModal.value = false;
    newProject.value = {
      name: "",
      description: "",
      tasks: [],
    };
  } catch (err) {
    console.error("Failed to create project:", err);
    alert("Failed to create project");
  }
};

onMounted(() => {
  loadProjects();
  loadTagsAndUsers();
});

const toggleTaskStatus = async (task: any) => {
  const newStatus = task.status === "done" ? "todo" : "done";

  try {
    const payload = {
      title: task.title,
      description: task.description,
      status: newStatus,
      due_date: task.due_date,
    };

    await updateTask(task.id, payload);
    task.status = newStatus;
  } catch (err) {
    console.error("Failed to update task:", err);
  }
};

const addTask = () => {
  newProject.value.tasks.push({
    title: "",
    description: "",
    status: "todo",
    tags: [] as number[],
    users: [] as number[],
  });
};

const removeTask = (index: number) => {
  newProject.value.tasks.splice(index, 1);
};

</script>

<!----------------------------------------->

<template>

<div class="projects-container">
  <h1>Projects</h1>
  <button class="add-btn" @click="showAddModal = true">+ Add Project</button>

  <div class="project-grid">
    <div v-for="project in projects" :key="project.id" class="project-card">
      <div class="project-header">
        <h2>{{ project.name }}</h2>
      </div>
      <p>{{ project.description }}</p>

      <!-- Task list -->
      <ul class="task-list">
        <li v-for="task in project.tasks || []" :key="task.id" class="task-item">
          
          <!-- First row: checkbox, title, tag -->
          <div class="task-top">
            <div class="task-left">
              <input
                type="checkbox"
                :checked="task.status === 'done'"
                @change="toggleTaskStatus(task)"
              />
              <strong>{{ task.title }}</strong>
            </div>
            <div class="task-right">
              <span
                v-for="tag in task.tags"
                :key="tag.id"
                class="priority"
                :style="{ backgroundColor: tag.color }"
              >
                {{ tag.name }}
              </span>
            </div>
          </div>

          <!-- Second row: description -->
          <div class="task-description" v-if="task.description">
            {{ task.description }}
          </div>

          <!-- Third row: assigned users -->
          <div class="task-bottom">
            <span
              v-for="assignment in task.assignments"
              :key="assignment.user.id"
              class="user"
            >
              @{{ assignment.user.username }}
            </span>
          </div>
        </li>
      </ul>


      <div class="card-buttons">
        <button @click="openUpdateModal(project)">Edit</button>
        <button @click="removeProject(project.id)">Delete</button>
      </div>
    </div>
  </div>
</div>


<!-- Add Project Modal -->
<div v-if="showAddModal" class="modal-overlay">
  <div class="modal-content">
    <h2>Add New Project</h2>
    <form @submit.prevent="addProject">
      <!-- Project name -->
      <div class="form-group">
        <label for="name">Name</label>
        <input id="name" v-model="newProject.name" type="text" required />
      </div>

      <!-- Project description -->
      <div class="form-group">
        <label for="description">Description</label>
        <textarea id="description" v-model="newProject.description" rows="4" required></textarea>
      </div>

      <!-- Tasks -->
      <div class="form-group">
        <label>Tasks</label>
        <div
          v-for="(task, index) in newProject.tasks"
          :key="index"
          class="task-input"
        >
          <h4>Task {{ index + 1 }}</h4>
          <input v-model="task.title" type="text" placeholder="Task title" required />
          <textarea v-model="task.description" placeholder="Task description"></textarea>

          <!-- Task status -->
          <select v-model="task.status">
            <option value="todo">To do</option>
            <option value="in_progress">In progress</option>
            <option value="done">Done</option>
          </select>

          <!-- Task tags -->
          <label>Tags</label>
          <select v-model="task.tags" multiple>
            <option v-for="tag in tags" :key="tag.id" :value="tag.id">{{ tag.name }}</option>
          </select>

          <!-- Task users -->
          <label>Assign Users</label>
          <select v-model="task.users" multiple>
            <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }}</option>
          </select>

          <!-- Remove task button -->
          <button type="button" class="secondary" @click="removeTask(index)">
            Remove Task
          </button>
        </div>

        <button type="button" class="secondary" @click="addTask">
          + Add Task
        </button>
      </div>

      <!-- Buttons -->
      <div class="modal-buttons">
        <button type="submit" class="primary">Create</button>
        <button type="button" class="secondary" @click="showAddModal = false">
          Cancel
        </button>
      </div>
    </form>
  </div>
</div>

<!-- Update Project Modal -->
<div v-if="showUpdateModal" class="modal-overlay">
  <div class="modal-content">
    <h2>Update Project</h2>
    <form @submit.prevent="saveProjectUpdate">
      <!-- Project name -->
      <div class="form-group">
        <label for="update-name">Name</label>
        <input id="update-name" v-model="selectedProject.name" type="text" required />
      </div>

      <!-- Project description -->
      <div class="form-group">
        <label for="update-description">Description</label>
        <textarea
          id="update-description"
          v-model="selectedProject.description"
          rows="4"
          required
        ></textarea>
      </div>

      <!-- Tasks -->
      <div class="form-group">
        <label>Tasks</label>
        <div
          v-for="(task, index) in selectedProject.tasks"
          :key="task.id || index"
          class="task-input"
        >
          <h4>Task {{ index + 1 }}</h4>
          <input v-model="task.title" type="text" placeholder="Task title" required />
          <textarea v-model="task.description" placeholder="Task description"></textarea>

          <!-- Task status -->
          <select v-model="task.status">
            <option value="todo">To do</option>
            <option value="in_progress">In progress</option>
            <option value="done">Done</option>
          </select>

          <!-- Task tags -->
          <label>Tags</label>
          <select v-model="task.tags" multiple>
            <option v-for="tag in tags" :key="tag.id" :value="tag.id">{{ tag.name }}</option>
          </select>

          <!-- Task users -->
          <label>Assign Users</label>
          <select v-model="task.users" multiple>
            <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }}</option>
          </select>

          <!-- Remove task button -->
          <button type="button" class="secondary" @click="removeTaskFromUpdate(index)">
            Remove Task
          </button>
        </div>

        <button type="button" class="secondary" @click="addTaskToUpdate">
          + Add Task
        </button>
      </div>

      <!-- Buttons -->
      <div class="modal-buttons">
        <button type="submit" class="primary">Save</button>
        <button type="button" class="secondary" @click="closeUpdateModal">
          Cancel
        </button>
      </div>
    </form>
  </div>
</div>

</template>


<style scoped>

/* --- Projects View --- */
.projects-container {
  text-align: center;
  padding: 2rem;
  color: white;
}

.add-btn {
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  background: #555;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 6px;
}

.project-grid {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
}

.project-card {
  background: #333;
  padding: 1rem;
  border-radius: 10px;
  width: 100%;
  width: 720px;
}

.project-header {
  margin-bottom: 0.5rem;
}

.task-list {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 0;
  list-style: none;
}

.task-item {
  background: #1f1f1f;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.task-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-left {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.task-left input[type="checkbox"] {
  transform: translateY(1px);
}

.task-left strong {
  font-size: 0.95rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: visible;
  text-overflow: clip;
  max-width: calc(100% - 20px);
  display: inline-block;
}

.task-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.4rem;
  min-width: 120px;
}

.task-bottom {
  margin-left: 2.4rem; 
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.task-description {
  margin-left: 2.4rem;
  font-size: 0.85rem;
  color: #ccc;
  white-space: pre-wrap;
}

.priority {
  font-size: 0.75rem;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  color: #fff;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

.user {
  font-size: 0.8rem;
  background: #444;
  color: #fff;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
}

.card-buttons {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
}

.card-buttons button {
  padding: 0.5rem 1rem;
  border: none;
  cursor: pointer;
  border-radius: 6px;
}

.card-buttons button:first-child {
  background: #555;
  color: white;
}

.card-buttons button:last-child {
  background: #e74c3c;
  color: white;
}

/* --- Modal Forms --- */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: #1e1e1e;
  color: #f0f0f0;
  padding: 2rem;
  border-radius: 12px;
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
  animation: fadeIn 0.25s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

h2 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  text-align: center;
  color: #fff;
}

.form-group {
  margin-bottom: 1.2rem;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 0.4rem;
  font-weight: bold;
  color: #ddd;
}

input,
textarea,
select {
  padding: 0.8rem;
  border: 1px solid #444;
  border-radius: 8px;
  background: #2a2a2a;
  color: #f0f0f0;
  font-size: 1rem;
  width: 100%;
  transition: border 0.2s, background 0.2s;
}

input:focus,
textarea:focus,
select:focus {
  border-color: #4caf50;
  outline: none;
  background: #333;
}

textarea {
  resize: vertical;
  min-height: 100px;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
  margin-top: 1.5rem;
}

.modal-buttons button {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s;
}

button.primary {
  background: #4caf50;
  color: white;
}
button.primary:hover {
  background: #43a047;
}

button.secondary {
  background: #555;
  color: white;
}
button.secondary:hover {
  background: #444;
}

</style>
