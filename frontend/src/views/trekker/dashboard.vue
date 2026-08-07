<template>
  <AppLayout title="Dashboard">

    <div class="row g-4">

      <DashboardCard
        title="Available Treks"
        :value="dashboard.available_treks"
        icon="bi bi-signpost-split"
      />

      <DashboardCard
        title="Booked Treks"
        :value="dashboard.booked_treks"
        icon="bi bi-journal-check"
      />

      <DashboardCard
        title="Completed"
        :value="dashboard.completed_treks"
        icon="bi bi-check-circle"
      />

      <DashboardCard
        title="Cancelled"
        :value="dashboard.cancelled_bookings"
        icon="bi bi-x-circle"
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
              <th>Trek</th>
              <th>Status</th>
              <th>Booking Date</th>
            </tr>
          </thead>

          <tbody v-if="dashboard.recentBookings.length">

            <tr
              v-for="booking in dashboard.recentBookings"
              :key="booking.id"
            >

              <td>{{ booking.id }}</td>

              <td>{{ booking.trek }}</td>

              <td>

                <span
                  class="badge"
                  :class="{
                    'bg-primary': booking.status === 'Booked',
                    'bg-success': booking.status === 'Completed',
                    'bg-danger': booking.status === 'Cancelled'
                  }"
                >
                  {{ booking.status }}
                </span>

              </td>

              <td>{{ formatDate(booking.date) }}</td>

            </tr>

          </tbody>

          <tbody v-else>

            <tr>

              <td
                colspan="4"
                class="text-center text-muted py-4"
              >
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
import api from "../../services/api"

const dashboard = ref({
  available_treks: 0,
  booked_treks: 0,
  completed_treks: 0,
  pending_bookings: 0,
  recentBookings: [],
})

const loadDashboard = async () => {
  try {
    const response = await api.get("/trekker/dashboard")
    dashboard.value = response.data
  } catch (error) {
    console.error(error.response?.data || error)
  }
}

onMounted(() => {
  loadDashboard()
})
</script>