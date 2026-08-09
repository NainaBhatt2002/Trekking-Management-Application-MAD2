<template>
  <nav class="navbar navbar-expand-lg bg-white border-bottom sticky-top px-4 py-2 shadow-sm">
    <div class="container-fluid px-0 d-flex align-items-center justify-content-between">
      
      <!-- Left: Sidebar Toggle & Page Title -->
      <div class="d-flex align-items-center gap-3">

        <!-- Mobile hamburger button -->
        <button
          class="btn btn-light border d-md-none p-1 d-flex align-items-center justify-content-center"
          @click="emit('toggle-sidebar')"
          title="Toggle Menu"
        >
          <i class="bi bi-list fs-3"></i>
        </button>

        <div>
          <h4 class="fw-bold mb-0 text-dark">{{ title }}</h4>
          <small class="text-secondary">
            Welcome, {{ welcomeRole }}!
          </small>
        </div>
      </div>



    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";

defineProps({
  title: {
    type: String,
    default: "Dashboard",
  },
  isSidebarCollapsed: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["toggle-sidebar"]);
const router = useRouter();

const currentTime = ref("");
let timer = null;

const updateClock = () => {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const logout = () => {
  localStorage.clear();
  router.push("/login");
};

const role = localStorage.getItem("role") || "user"

const welcomeRole =
  role.charAt(0).toUpperCase() + role.slice(1)

onMounted(() => {
  updateClock();
  timer = setInterval(updateClock, 1000);
});

onUnmounted(() => {
  if (timer) clearInterval(timer);
});
</script>