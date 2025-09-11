<script setup lang="ts">
import ProjectsView from './components/ProjectsView.vue';
</script>

<template>
  <div id="app">
    <!-- Navbar Component -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">urob.to</a>
        <ul class="navbar-nav me-auto mb-2 ml-lg-0">
          <li class="nav-item">
            <a class="nav-link" aria-current="page" href="#">Prehľad</a>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Main Content -->
    <div id="content" class="container mt-4">
      <ProjectsView />
    </div>
  </div>
</template>

<style scoped>
/* Add some basic styling to ensure navbar is visible */
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
}

#content {
  padding-top: 20px;
}
</style>
