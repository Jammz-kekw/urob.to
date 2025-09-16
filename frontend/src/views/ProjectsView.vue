<script setup lang="ts">
import { ref, onMounted, reactive } from "vue";
import { getProjects, deleteProject, createProject, updateTask } from "../services/api";

const projects = ref<any[]>([]);
const showAddModal = ref(false); // new: modal visibility
const newProject = ref({
  name: "",
  description: "",
});

const loadProjects = async () => {
  try {
    const res = await getProjects();
    projects.value = res.data;
  } catch (err) {
    console.error("Failed to load projects:", err);
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
    const res = await createProject(newProject.value);
    projects.value.push(res.data); // add new project to list
    showAddModal.value = false; // close modal
    newProject.value = { name: "", description: "" }; // reset form
  } catch (err) {
    console.error("Failed to create project:", err);
    alert("Failed to create project");
  }
};

onMounted(loadProjects());

const toggleTaskStatus = async (task: any) => {
  // Flip status
  const newStatus = task.status === "done" ? "todo" : "done";

  try {
    // Build a payload that matches TaskUpdate
    const payload = {
      title: task.title,
      description: task.description,
      status: newStatus,
      due_date: task.due_date,
    };

    await updateTask(task.id, payload);

    // Update locally so UI reflects immediately
    task.status = newStatus;
  } catch (err) {
    console.error("Failed to update task:", err);
  }
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

    <!-- Add Project Modal -->
    <div v-if="showAddModal" class="modal-overlay">
      <div class="modal">
        <h2>Add New Project</h2>
        <form @submit.prevent="addProject">
          <div>
            <label for="name">Name</label>
            <input id="name" v-model="newProject.name" type="text" required />
          </div>
          <div>
            <label for="description">Description</label>
            <textarea id="description" v-model="newProject.description" required></textarea>
          </div>
          <div class="modal-buttons">
            <button type="submit">Create</button>
            <button type="button" @click="showAddModal = false">Cancel</button>
          </div>
        </form>
      </div>
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
}
.modal {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 400px;
  max-width: 90%;
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
</style>
