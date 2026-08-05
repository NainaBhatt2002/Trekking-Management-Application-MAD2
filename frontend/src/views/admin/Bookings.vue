<template>

  <AdminLayout title="Bookings">

    <div class="d-flex justify-content-between align-items-center mb-4">

      <h3 class="fw-bold mb-0">
        Manage all Bookings
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
              <th>Booking Date</th>
              <th>Booking Status</th>
              <th>Payment</th>
              <th class="text-center">Actions</th>
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

              <td>{{ booking.booking_date }}</td>

              <td>

                <span
                  class="badge"
                  :class="
                    booking.booking_status === 'Confirmed'
                      ? 'bg-success'
                      : booking.booking_status === 'Pending'
                      ? 'bg-warning text-dark'
                      : 'bg-danger'
                  "
                >
                  {{ booking.booking_status }}
                </span>

              </td>

              <td>

                <span
                  class="badge"
                  :class="
                    booking.payment_status === 'Paid'
                      ? 'bg-success'
                      : 'bg-warning text-dark'
                  "
                >
                  {{ booking.payment_status }}
                </span>

              </td>

              <td class="text-center">

                <button
                  class="btn btn-sm btn-outline-primary"
                  @click="openModal(booking)"
                >
                  <i class="bi bi-eye"></i>
                </button>

              </td>

            </tr>

          </tbody>

          <tbody v-else>

            <tr>

              <td
                colspan="7"
                class="text-center text-muted py-5"
              >
                No bookings found.
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

    <!-- Booking Details Modal -->

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
              <strong>Booking Date:</strong>
              {{ selectedBooking.booking_date }}
            </p>

            <p>
              <strong>Booking Status:</strong>
              {{ selectedBooking.booking_status }}
            </p>

            <p>
              <strong>Payment Status:</strong>
              {{ selectedBooking.payment_status }}
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

  </AdminLayout>

</template>

<script setup>
import { ref, computed, onMounted } from "vue";

import api from "../../services/api";
import AdminLayout from "../../components/AdminLayout.vue";
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

onMounted(() => {
  loadBookings();
});
</script>