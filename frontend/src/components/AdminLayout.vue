<script setup>
import { ref } from "vue";
import Sidebar from "./Sidebar.vue";
import Navbar from "./Navbar.vue";

defineProps({
  title: {
    type: String,
    default: "Dashboard",
  },
});

const isCollapsed = ref(localStorage.getItem("admin_sidebar_collapsed") === "true");

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
  localStorage.setItem("admin_sidebar_collapsed", isCollapsed.value);
};
</script>

<template>
  <div class="d-flex min-vh-100 bg-light">
    <!-- Full-Height Sidebar Container -->
    <aside class="position-sticky top-0 vh-100 flex-shrink-0 z-3">
      <Sidebar :is-collapsed="isCollapsed" @toggle="toggleSidebar" />
    </aside>

    <!-- Main Content Area -->
    <div class="flex-grow-1 d-flex flex-column min-w-0">
      <Navbar :title="title" :is-sidebar-collapsed="isCollapsed"/>

      <main class="container-fluid p-4 flex-grow-1">
        <slot />
      </main>
    </div>
  </div>
</template>

