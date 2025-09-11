<script setup lang="ts">
import { ref, onMounted } from "vue";
import { fetchProjects, addProject } from "../api";

// Reactive references
const projects = ref<any[]>([]);
const newProject = ref("");
const isLoading = ref(false);  // Loading state
const errorMessage = ref("");  // Error state

// Load projects from the API
async function loadProjects() {
  isLoading.value = true;  // Set loading state to true
  errorMessage.value = "";  // Reset error message
  try {
    projects.value = await fetchProjects();
  } catch (err) {
    console.error("Error loading projects:", err);
    errorMessage.value = "Failed to load projects. Please try again later.";  // Show error message to the user
  } finally {
    isLoading.value = false;  // Set loading state to false after fetching
  }
}

// Create a new project
async function createProject() {
  if (!newProject.value.trim()) return; // Check for empty input
  try {
    const project = await addProject(newProject.value);
    projects.value.push(project);
    newProject.value = ""; // Clear input after successful creation
  } catch (err) {
    console.error("Error creating project:", err);
    errorMessage.value = "Failed to create project. Please try again later.";  // Show error message on failure
  }
}

onMounted(loadProjects);
</script>

<template>
  <div class="projects">
    <h2>Projects</h2>

    <!-- Loading Indicator -->
    <div v-if="isLoading" class="loading">Loading projects...</div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <!-- Projects List -->
    <ul v-if="projects.length && !isLoading">
      <li v-for="p in projects" :key="p.id">{{ p.name }}</li>
    </ul>

    <!-- No Projects Found -->
    <p v-else>No projects found.</p>

    <!-- Add New Project Form -->
    <div class="add-project">
      <input
        v-model="newProject"
        placeholder="Enter new project name"
        :disabled="isLoading"
      />
      <button @click="createProject" :disabled="isLoading || !newProject.trim()">Add Project</button>
    </div>
  </div>
</template>

<style scoped>
.projects {
  padding: 1rem;
}

.loading {
  color: #007bff;
}

.error {
  color: red;
  font-weight: bold;
}

.add-project {
  margin-top: 1rem;
}

input {
  padding: 0.3rem;
  margin-right: 0.5rem;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 0.3rem 0.5rem;
  cursor: pointer;
}

button:hover {
  background-color: #218838;
}
</style>
