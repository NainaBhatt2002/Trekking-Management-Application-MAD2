<script setup>
import { useRouter, useRoute } from "vue-router";

defineProps({
  isCollapsed: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["toggle"]);
const router = useRouter();
const route = useRoute();

const navItems = [
  { path: "/admin/dashboard", label: "Dashboard", icon: "bi bi-speedometer2" },
  { path: "/admin/treks", label: "Treks", icon: "bi bi-signpost-split" },
  { path: "/admin/staff", label: "Staff", icon: "bi bi-person-badge" },
  { path: "/admin/users", label: "Users", icon: "bi bi-people" },
  { path: "/admin/bookings", label: "Bookings", icon: "bi bi-journal-check" },
  { path: "/admin/reports", label: "Reports", icon: "bi bi-bar-chart" },
];

const isActive = (path) => route.path === path;

function logout() {
  localStorage.clear();
  router.push("/login");
}
</script>

<template>
  <div
    class="bg-dark text-white p-3 d-flex flex-column h-100 shadow"
    :style="{ width: isCollapsed ? '80px' : '250px' }"
  >
    <!-- Brand Header & Three Lines Toggle Button -->
    <div
      class="d-flex align-items-center mb-3"
      :class="isCollapsed ? 'flex-column gap-3 align-items-center' : 'justify-content-between px-1'"
    >
      <div class="d-flex align-items-center gap-2 overflow-hidden">
        <div class="bg-primary text-white rounded p-2 d-flex align-items-center justify-content-center" style="width: 38px; height: 38px;">
          <i class="bi bi-tree-fill fs-5"></i>
        </div>
        <h4 v-if="!isCollapsed" class="fw-bold mb-0 text-white text-nowrap">Trekkify</h4>
      </div>

      <!-- Three lines button inside sidebar header -->
      <button
        type="button"
        class="btn btn-dark text-white-50 border-0 p-1 d-flex align-items-center justify-content-center"
        @click="emit('toggle')"
        title="Toggle Navigation Menu"
      >
        <i class="bi bi-list fs-3"></i>
      </button>
    </div>

    <hr class="border-secondary my-2 opacity-50" />

    <!-- Navigation Menu -->
    <ul class="nav nav-pills flex-column mb-auto gap-1">
      <li v-for="item in navItems" :key="item.path" class="nav-item">
        <router-link
          :to="item.path"
          class="nav-link text-white d-flex align-items-center py-2 px-3 rounded"
          :class="[
            isActive(item.path) ? 'active bg-primary fw-bold' : '',
            isCollapsed ? 'justify-content-center px-0' : 'gap-3'
          ]"
          :title="isCollapsed ? item.label : ''"
        >
          <i :class="[item.icon, 'fs-5']"></i>
          <span v-if="!isCollapsed" class="text-nowrap">{{ item.label }}</span>
        </router-link>
      </li>
    </ul>

    <hr class="border-secondary my-2 opacity-50" />

    <!-- Logout Button -->
    <div class="mt-auto">
      <button
        class="btn btn-outline-danger w-100 d-flex align-items-center justify-content-center py-2"
        :class="isCollapsed ? 'px-0' : 'gap-2'"
        @click="logout"
        :title="isCollapsed ? 'Logout' : ''"
      >
        <i class="bi bi-box-arrow-right fs-5"></i>
        <span v-if="!isCollapsed">Logout</span>
      </button>
    </div>
  </div>
</template>

