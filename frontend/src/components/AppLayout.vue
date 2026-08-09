<template>
  <div class="d-flex min-vh-100 bg-light">

    <!-- Mobile Overlay Backdrop -->
    <div
      v-if="isMobile && !isCollapsed"
      class="sidebar-overlay"
      @click="closeSidebar"
    ></div>

    <!-- Full-Height Sidebar Container -->
    <aside
      class="flex-shrink-0"
      :class="isMobile ? 'sidebar-mobile' : 'position-sticky top-0 vh-100 z-3'"
      :style="{ display: isMobile && isCollapsed ? 'none' : 'block' }"
    >
      <Sidebar :is-collapsed="isMobile ? false : isCollapsed" @toggle="toggleSidebar" />
    </aside>

    <!-- Main Content Area -->
    <div class="flex-grow-1 d-flex flex-column min-w-0">
      <Navbar :title="title" :is-sidebar-collapsed="isCollapsed" @toggle-sidebar="toggleSidebar" />

      <main class="container-fluid p-4 flex-grow-1">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import Sidebar from "./Sidebar.vue";
import Navbar from "./Navbar.vue";

const route = useRoute()

defineProps({
  title: {
    type: String,
    default: "Dashboard",
  },
});

const MOBILE_BREAKPOINT = 768

const isMobile = ref(window.innerWidth <= MOBILE_BREAKPOINT)

const isCollapsed = ref(
  isMobile.value
    ? true
    : localStorage.getItem("sidebar_collapsed") === "true"
)

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
  if (!isMobile.value) {
    localStorage.setItem(
      "sidebar_collapsed",
      isCollapsed.value
    )
  }
}

const closeSidebar = () => {
  isCollapsed.value = true
}

// Auto-close sidebar on mobile when navigating
watch(() => route.path, () => {
  if (isMobile.value) {
    isCollapsed.value = true
  }
})

const handleResize = () => {
  const wasMobile = isMobile.value
  isMobile.value = window.innerWidth <= MOBILE_BREAKPOINT

  if (isMobile.value && !wasMobile) {
    // Switched to mobile — collapse sidebar
    isCollapsed.value = true
  } else if (!isMobile.value && wasMobile) {
    // Switched to desktop — restore saved preference
    isCollapsed.value = localStorage.getItem("sidebar_collapsed") === "true"
  }
}

onMounted(() => {
  window.addEventListener("resize", handleResize)
})

onUnmounted(() => {
  window.removeEventListener("resize", handleResize)
})
</script>

<style scoped>
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1040;
}

.sidebar-mobile {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 250px;
  z-index: 1050;
  box-shadow: 4px 0 16px rgba(0, 0, 0, 0.3);
}
</style>