<template>
  <form @submit.prevent="submit">
    <input v-model="title" placeholder="Task title" required />
    <input v-model="description" placeholder="Description" />
    <button type="submit">Add Task</button>
  </form>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { createTask } from "../services/api";

const props = defineProps<{ projectId: number }>();
const emit = defineEmits(["created"]);

const title = ref("");
const description = ref("");

async function submit() {
  await createTask({
    project_id: props.projectId,
    title: title.value,
    description: description.value,
  });
  title.value = "";
  description.value = "";
  emit("created");
}
</script>
