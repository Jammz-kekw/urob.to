<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getProjects, deleteProject, createProject, updateProject, updateTask, getTags, getUsers } from "../services/api";
import type { ProjectPayload } from "../services/api";

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
    tags?: number[];  // tag IDs
    users?: number[]; // user IDs
  }[],
});

const openUpdateModal = (project: any) => {
  // normalize tags + assignments into ID arrays
  selectedProject.value = {
    ...project,
    tasks: project.tasks.map((t: any) => ({
      ...t,
      tags: t.tags.map((tag: any) => tag.id),              // keep only IDs
      users: t.assignments.map((a: any) => a.user.id)      // keep only IDs
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
      tags: task.tags,   // IDs only
      users: task.users  // IDs only
    }))
  };

  try {
    const res = await updateProject(selectedProject.value.id, payload);

    // Update local list
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
    // Only include valid tasks
    const filteredTasks = newProject.value.tasks
      .filter(t => t.title.trim() !== "")
      .map(task => ({
        title: task.title,
        description: task.description || "",
        status: task.status || "todo",
        tags: task.tags || [],   // tag IDs per task
        users: task.users || []  // user IDs per task
      }));

    const payload = {
      name: newProject.value.name,
      description: newProject.value.description,
      tasks: filteredTasks
    };

    const res = await createProject(payload);

    // Add the new project to the local list
    projects.value.push(res.data);

    // Close modal and reset form
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
    tags: [] as number[],   // store tag IDs
    users: [] as number[],  // store user IDs
  });
};

const removeTask = (index: number) => {
  newProject.value.tasks.splice(index, 1);
};

</script>


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
        <ul>
          <li v-for="task in project.tasks || []" :key="task.id">
            <input
              type="checkbox"
              :checked="task.status === 'done'"
              @change="toggleTaskStatus(task)"
            />
            {{ task.title }}
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
  <div class="modal">
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
  <div class="modal">
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
.projects-container {
  padding: 1.5rem;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); /* wider cards */
  gap: 1rem;
}

.project-card {
  background: #747474;
  border-radius: 12px;
  padding: 1.5rem; /* a bit more padding */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

/* Task list adjustments */
.project-card ul {
  list-style: none; /* remove dots */
  padding: 0;
  margin: 0.5rem 0;
}

.project-card li {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.project-card li input[type="checkbox"] {
  margin-right: 0.5rem; /* space between checkbox and text */
}

/* Buttons at the bottom */
.card-buttons {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.card-buttons button {
  flex: 1;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.card-buttons button:first-child {
  background-color: #6c757d; /* grey for edit */
  color: white;
}

.card-buttons button:last-child {
  background-color: #dc3545; /* red for delete */
  color: white;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  overflow: auto; /* ✅ allow scrolling if modal is taller than screen */
}

.modal {
  background: #1e1e1e; /* dark theme background */
  color: #f0f0f0;
  padding: 2rem;
  border-radius: 12px;
  width: 500px;
  max-width: 90%;
  max-height: 90vh;   /* ✅ don't exceed viewport */
  overflow-y: auto;   /* ✅ scrollable inside modal */
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}
.modal button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.modal button[type="submit"] {
  background: #4caf50;
  color: white;
}
.modal button[type="button"] {
  background: #747474;
} 

.modal {
  background: #1e1e1e; /* dark theme background */
  color: #f0f0f0; /* light text */
  padding: 2rem;
  border-radius: 12px;
  width: 500px;
  max-width: 90%;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
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
}

input:focus,
textarea:focus,
select:focus {
  border-color: #4caf50;
  outline: none;
}

.task-input {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
  margin-top: 1rem;
}

button.primary {
  background: #4caf50;
  color: white;
  font-weight: bold;
}

button.secondary {
  background: #555;
  color: white;
}

button {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  opacity: 0.9;
}

.card-buttons {
  display: flex;
  gap: 0.5rem; /* spacing between buttons */
  margin-top: 1rem;
}

.card-buttons button {
  flex: 1; /* equal width */
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s ease;
}

/* Grey edit button */
.btn-edit {
  background-color: #6c757d; /* grey */
  color: white;
}
.btn-edit:hover {
  background-color: #5a6268;
}

/* Red delete button */
.btn-delete {
  background-color: #dc3545; /* red */
  color: white;
}
.btn-delete:hover {
  background-color: #c82333;
}

</style>
