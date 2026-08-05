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
    <!-- Sticky Full-Height Sidebar Container -->
    <aside class="position-sticky top-0 vh-100 flex-shrink-0 z-3">
      <Sidebar :is-collapsed="isCollapsed" @toggle="toggleSidebar" />
    </aside>


    <!-- Main Content Area -->
    <div class="flex-grow-1 d-flex flex-column min-w-0">
      <Navbar :title="title" :is-sidebar-collapsed="isCollapsed" @toggle-sidebar="toggleSidebar" />

      <main class="container-fluid p-4 flex-grow-1">
        <slot />
      </main>

      <footer class="bg-white border-top py-3 text-center text-secondary small">
        &copy; 2026 <strong>Trekkify</strong> - Trekking Management Application. All rights reserved.
      </footer>
    </div>
  </div>
</template>
