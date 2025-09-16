<template>
  <form @submit.prevent="submit">
    <input v-model="name" placeholder="Project name" required />
    <input v-model="description" placeholder="Description" />
    <button type="submit">Add Project</button>
  </form>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { createProject } from "../services/api";

const emit = defineEmits(["created"]);

const name = ref("");
const description = ref("");

async function submit() {
  await createProject({ name: name.value, description: description.value });
  name.value = "";
  description.value = "";
  emit("created");
}
</script>
