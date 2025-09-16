<template>
  <div id="app">
    <h1 id="page-title">
      urob<span class="dot">.</span>to
    </h1>
    <ProjectsView />
  </div>
</template>

<script setup lang="ts">
import ProjectsView from "./views/ProjectsView.vue";
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  padding: 2rem; /* this is fine for content */
}

/* Fix: make the title fixed in the viewport top-left */
#page-title {
  position: fixed; /* fixed to viewport */
  top: 10px;
  left: 10px;
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
  z-index: 1000; /* ensures it's above other content */
}

/* Dot color */
#page-title .dot {
  color: red;
}
</style>
