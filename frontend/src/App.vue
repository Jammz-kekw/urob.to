<!-- 
  Root app component
  - renders the main page with the ProjectsView
  - serves as entry point of the Vue app
-->

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
  padding: 2rem;
}

#page-title {
  position: fixed; 
  top: 10px;
  left: 10px;
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
  z-index: 1000;
}

/* Dot color */
#page-title .dot {
  color: red;
}
</style>
