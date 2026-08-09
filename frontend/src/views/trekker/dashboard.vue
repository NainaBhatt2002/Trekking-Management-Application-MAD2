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
              <th>Trek Name</th>
              <th>Location</th>
              <th>Trek Date</th>
              <th>Booking Status</th>
              <th>Trek Status</th>
            </tr>
          </thead>

          <tbody v-if="dashboard.recentBookings.length">

            <tr
              v-for="booking in dashboard.recentBookings"
              :key="booking.id"
            >

              <td>{{ booking.trek }}</td>

              <td>{{ booking.location }}</td>

              <td>{{ formatDate(booking.trek_date) }}</td>

              <td>

                <span
                  class="badge"
                  :class="{
                    'bg-primary': booking.booking_status === 'Booked',
                    'bg-success': booking.booking_status === 'Completed',
                    'bg-danger': booking.booking_status === 'Cancelled'
                  }"
                >
                  {{ booking.booking_status }}
                </span>

              </td>

              <td>

                <span
                  class="badge"
                  :class="{
                    'bg-success': booking.trek_status === 'Open',
                    'bg-warning text-dark': booking.trek_status === 'Started',
                    'bg-secondary': booking.trek_status === 'Closed',
                    'bg-dark': booking.trek_status === 'Completed'
                  }"
                >
                  {{ booking.trek_status }}
                </span>

              </td>

            </tr>

          </tbody>

          <tbody v-else>

            <tr>

              <td
                colspan="5"
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

const formatDate = (date) => {
  if (!date) return "N/A"

  return new Date(date).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric"
  })
}

onMounted(() => {
  loadDashboard()
})
</script>