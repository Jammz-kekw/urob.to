<template>
  <div>
    <h3>Tasks</h3>
    <TaskForm :projectId="projectId" @created="loadTasks" />
    <ul>
      <li v-for="task in tasks" :key="task.id">
        <input type="checkbox" :checked="task.status === 'done'" @change="toggleStatus(task)" />
        {{ task.title }} — {{ task.description }}
        <button @click="deleteTaskFn(task.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getTasks, updateTask, deleteTask } from "../services/api";
import TaskForm from "./TaskForm.vue";

const props = defineProps<{ projectId: number }>();
const tasks = ref<any[]>([]);

async function loadTasks() {
  const res = await getTasks(props.projectId);
  tasks.value = res.data.tasks || [];
}

async function toggleStatus(task: any) {
  const newStatus = task.status === "done" ? "todo" : "done";
  await updateTask(task.id, { ...task, status: newStatus });
  loadTasks();
}

async function deleteTaskFn(id: number) {
  await deleteTask(id);
  loadTasks();
}

onMounted(loadTasks);
</script>
