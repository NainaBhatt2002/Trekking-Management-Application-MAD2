<template>

  <AppLayout title="My Bookings">

    <div class="card shadow-sm border-0 rounded-4">

      <div class="card-header bg-white">

        <h5 class="mb-0">
          My Trek Bookings
        </h5>

      </div>

      <div class="card-body">

        <table class="table table-hover align-middle">

          <thead>

            <tr>
              <th>Trek</th>
              <th>Location</th>
              <th>Difficulty</th>
              <th>Duration</th>
              <th>Booking Status</th>
              <th>Trek Status</th>
              <th>Booking Date</th>
            </tr>

          </thead>

          <tbody v-if="bookings.length">

            <tr
              v-for="booking in bookings"
              :key="booking.id"
            >

              <td>{{ booking.trek_name }}</td>

              <td>{{ booking.location }}</td>

              <td>

                <span
                  class="badge"
                  :class="{
                    'bg-success': booking.difficulty === 'Easy',
                    'bg-warning text-dark': booking.difficulty === 'Moderate',
                    'bg-danger': booking.difficulty === 'Hard'
                  }"
                >
                  {{ booking.difficulty }}
                </span>

              </td>

              <td>{{ booking.duration }} Days</td>

              <td>

                <span
                  class="badge"
                  :class="{
                    'bg-warning text-dark': booking.booking_status === 'Pending',
                    'bg-success': booking.booking_status === 'Confirmed',
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
                    'bg-danger': booking.trek_status === 'Closed',
                    'bg-primary': booking.trek_status === 'Started',
                    'bg-dark': booking.trek_status === 'Completed'
                  }"
                >
                  {{ booking.trek_status }}
                </span>

              </td>

              <td>{{ booking.booking_date }}</td>

            </tr>

          </tbody>

          <tbody v-else>

            <tr>

              <td
                colspan="7"
                class="text-center text-muted py-5"
              >

                <i class="bi bi-journal-x fs-1 d-block mb-3"></i>

                You haven't booked any treks yet.

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
import api from "../../services/api"

const bookings = ref([])

const loadBookings = async () => {
  try {

    const response = await api.get("/trekker/bookings")

    bookings.value = response.data

  } catch (error) {
    console.error(error.response?.data || error)
  }
}

onMounted(() => {
  loadBookings()
})
</script>