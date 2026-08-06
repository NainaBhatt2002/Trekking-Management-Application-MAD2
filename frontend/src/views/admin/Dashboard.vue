<template>
  <AppLayout title="Admin Dashboard">

    <div class="row g-4">

      <DashboardCard
        title="Treks"
        :value="dashboard.total_treks"
        icon="bi bi-signpost-split"
      />

      <DashboardCard
        title="Users"
        :value="dashboard.total_users"
        icon="bi bi-people"
      />

      <DashboardCard
        title="Staff"
        :value="dashboard.total_staff"
        icon="bi bi-person-badge"
      />

      <DashboardCard
        title="Bookings"
        :value="dashboard.total_bookings"
        icon="bi bi-journal-check"
      />

    </div>

    <div class="card mt-5 shadow-sm border-0 rounded-4">

      <div class="card-header bg-white">
        <h5 class="mb-0">Recent Bookings</h5>
      </div>

      <div class="card-body">

        <table class="table table-hover align-middle">

          <thead>
            <tr>
              <th>ID</th>
              <th>User</th>
              <th>Trek</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody v-if="dashboard.recentBookings.length">

            <tr
              v-for="booking in dashboard.recentBookings"
              :key="booking.id"
            >
              <td>{{ booking.id }}</td>
              <td>{{ booking.user }}</td>
              <td>{{ booking.trek }}</td>
              <td>
                <span class="badge bg-success">
                  {{ booking.status }}
                </span>
              </td>
            </tr>

          </tbody>

          <tbody v-else>

            <tr>
              <td colspan="4" class="text-center text-muted py-4">
                No bookings available.
              </td>
            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue"
import AppLayout from "../../components/AppLayout.vue"
import DashboardCard from "../../components/DashboardCard.vue"
import api from "../../services/api.js"

const dashboard = ref({
  total_treks: 0,
  total_users: 0,
  total_staff: 0,
  total_bookings: 0,
  recentBookings: [],
})

const loadDashboard = async () => {
  try {
    const response = await api.get("/admin/dashboard")
    dashboard.value = response.data
  } catch (error) {
    console.error(error.response?.data || error)
  }
}

onMounted(() => {
  loadDashboard()
})
</script>