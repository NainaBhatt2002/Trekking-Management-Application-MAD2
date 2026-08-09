<template>

  <AppLayout title="Bookings">

    <div class="d-flex justify-content-between align-items-center mb-4">

      <h3 class="fw-bold mb-0">
        View all Bookings
      </h3>

    </div>

    <SearchBar
      v-model="search"
      class="mb-4"
      placeholder="Search by Booking ID, Trek or User..."
    />

    <div class="card border-0 shadow-sm rounded-4">

      <div class="card-body">

        <table class="table table-hover align-middle">

          <thead>

          <tr>
            <th>ID</th>
            <th>User</th>
            <th>Trek</th>
            <th>Staff</th>
            <th>Booking Date</th>
            <th>Booking Status</th>
            <th>Trek Status</th>
            <th>Trek Date</th>
            <th class="text-center">Details</th>
          </tr>

          </thead>

          <tbody v-if="filteredBookings.length">

            <tr
              v-for="booking in filteredBookings"
              :key="booking.id"
            >

              <td>{{ booking.id }}</td>

              <td>{{ booking.user }}</td>

              <td>{{ booking.trek }}</td>

              <td>{{ booking.staff }}</td>

              <td>{{ formatDate(booking.booking_date) }}</td>

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

              <td>
                {{ formatDate(booking.trek_date) }}
              </td>

              <td class="text-center">

                <button
                  class="btn btn-sm btn-outline-primary"
                  @click="openModal(booking)"
                >
                  <i class="bi bi-eye"></i>
                  View
                </button>

              </td>

            </tr>

          </tbody>

          <tbody v-else>

            <tr>

              <td
                colspan="9"
                class="text-center text-muted py-5"
              >
                No bookings found.
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

    <!-- Booking Details Pop up -->

    <div
      v-if="showModal"
      class="modal fade show"
      style="display:block;background:rgba(0,0,0,.5);"
    >

      <div class="modal-dialog">

        <div class="modal-content">

          <div class="modal-header">

            <h5 class="modal-title">
              Booking Details
            </h5>

            <button
              class="btn-close"
              @click="closeModal"
            ></button>

          </div>

          <div class="modal-body">

            <p>
              <strong>Booking ID:</strong>
              {{ selectedBooking.id }}
            </p>

            <p>
              <strong>User:</strong>
              {{ selectedBooking.user }}
            </p>

            <p>
              <strong>Email:</strong>
              {{ selectedBooking.email }}
            </p>

            <p>
              <strong>Trek:</strong>
              {{ selectedBooking.trek }}
            </p>
            <p>
            <strong>Staff:</strong>
            {{ selectedBooking.staff }}
            </p>

            <p>
              <strong>Location:</strong>
              {{ selectedBooking.location }}
            </p>

            <p>
              <strong>Difficulty:</strong>
              {{ selectedBooking.difficulty }}
            </p>

            <p>
              <strong>Duration:</strong>
              {{ selectedBooking.duration }} Days
            </p>

            <p>
              <strong>Trek Date:</strong>
              {{ formatDate(selectedBooking.trek_date) }}
            </p>

            <p>
              <strong>Booking Date:</strong>
              {{ formatDate(selectedBooking.booking_date) }}
            </p>

            <p>
              <strong>Booking Status:</strong>
              {{ selectedBooking.booking_status }}
            </p>

            <p>
              <strong>Trek Status:</strong>
              {{ selectedBooking.trek_status }}
            </p>

          </div>

          <div class="modal-footer">

            <button
              class="btn btn-secondary"
              @click="closeModal"
            >
              Close
            </button>

          </div>

        </div>

      </div>

    </div>

  </AppLayout>

</template>

<script setup>
import { ref, computed, onMounted } from "vue";

import api from "../../services/api";
import AppLayout from "../../components/AppLayout.vue";
import SearchBar from "../../components/SearchBar.vue";

const bookings = ref([]);
const search = ref("");
const showModal = ref(false);
const selectedBooking = ref(null);
const filteredBookings = computed(() => {
  const query = search.value.toLowerCase().trim();

  return bookings.value.filter((booking) =>
    booking.id.toString().includes(query) ||
    booking.user.toLowerCase().includes(query) ||
    booking.trek.toLowerCase().includes(query)
  );
});

const loadBookings = async () => {
  try {

    const response = await api.get("/admin/bookings");

    console.log(response.data);

    bookings.value = response.data;

  } catch (error) {
    console.error(error.response?.data || error);
  }
};

const openModal = (booking) => {
  selectedBooking.value = booking;
  showModal.value = true;
};

const closeModal = () => {
  selectedBooking.value = null;
  showModal.value = false;
};

const formatDate = (date) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  })
}

onMounted(() => {
  loadBookings();
});
</script>