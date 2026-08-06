<template>
  <AppLayout title="Staff Dashboard">

    <div class="row g-4">

      <DashboardCard
        title="Assigned Treks"
        :value="dashboard.assigned_treks"
        icon="bi bi-signpost-split"
      />

      <DashboardCard
        title="Trekkers"
        :value="dashboard.registered_trekkers"
        icon="bi bi-people"
      />

      <DashboardCard
        title="Open Treks"
        :value="dashboard.open_treks"
        icon="bi bi-unlock"
      />

      <DashboardCard
        title="Started"
        :value="dashboard.started_treks"
        icon="bi bi-play-circle"
      />

      <DashboardCard
        title="Completed"
        :value="dashboard.completed_treks"
        icon="bi bi-check-circle"
      />

    </div>

  </AppLayout>
</template>


<script setup>
import { ref, onMounted } from "vue"
import AppLayout from "../../components/AppLayout.vue"
import DashboardCard from "../../components/DashboardCard.vue"
import api from "../../services/api.js"

const dashboard = ref({
  assigned_treks: 0,
  registered_trekkers: 0,
  open_treks: 0,
  started_treks: 0,
  completed_treks: 0,
})

const loadDashboard = async () => {
  try {
    const response = await api.get("/staff/dashboard")
    dashboard.value = response.data
  } catch (error) {
    console.error(error.response?.data || error)
  }
}

onMounted(loadDashboard)
</script>