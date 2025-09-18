<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getProjects, deleteProject, createProject, updateTask, getTags, getUsers } from "../services/api";

const projects = ref<any[]>([]);
const tags = ref<any[]>([]);
const users = ref<any[]>([]);
const showAddModal = ref(false);

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
        <button @click="removeProject(project.id)">Delete</button>
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
            <option value="todo">To Do</option>
            <option value="done">In progress</option>
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
</template>

<style scoped>
.projects-container {
  padding: 1.5rem;
}
.add-btn {
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}
.project-card {
  background: #747474;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
</style>
