<template>

  <AppLayout title="My Bookings">

    <div class="card shadow-sm border-0 rounded-4">

      <div class="card-header bg-white d-flex justify-content-between align-items-center">
        <h5 class="mb-0">
          My Trek Bookings
        </h5>

        <button
          class="btn btn-primary btn-sm"
          @click="exportHistory"
          :disabled="exporting"
        >
          <i
            class="bi"
            :class="exporting ? 'bi-hourglass-split' : 'bi-download'"
          ></i>
          {{ exporting ? "Exporting..." : "Export History" }}
        </button>
      </div>

      <div class="card-body">

        <table class="table table-hover align-middle">

          <thead>

            <tr>
              <th>Trek name</th>
              <th>Location</th>
              <th>Difficulty</th>
              <th>Duration</th>
              <th>Trek Date</th>
              <th>Booking Status</th>
              <th>Trek Status</th>
            </tr>

          </thead>

          <tbody v-if="bookings.length">

        <tr
        v-for="booking in bookings"
        :key="booking.id"
        >

        <td>
            {{ booking.trek_name }}
        </td>

        <td>
            {{ booking.location }}
        </td>

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

        <td>
            {{ booking.duration }} Days
        </td>

        <td>
            {{ formatDate(booking.trek_date) }}
        </td>

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

            <tr v-if="bookings.length === 0">

            <td
                colspan="7"
                class="text-center py-5 text-muted"
            >

                <i class="bi bi-journal-x fs-2 d-block mb-2"></i>

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
const exporting = ref(false)

const loadBookings = async () => {
  try {

    const response = await api.get("/trekker/bookings")

    bookings.value = response.data

  } catch (error) {
    console.error(error.response?.data || error)
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  })
}

const exportHistory = async () => {
  try {
    exporting.value = true;
    const response = await api.post("/trekker/export-history");
    const taskId = response.data.task_id;
    let completed = false;

    while (!completed) {
      await new Promise(resolve => setTimeout(resolve, 1000));

      const statusResponse = await api.get(
        `/trekker/export-history/status/${taskId}`
      );

      if (statusResponse.data.status === "Completed") {
        completed = true;
      } else if (statusResponse.data.status === "Failed") {
        throw new Error("Export failed.");
      }
    }

    const downloadResponse = await api.get(
      `/trekker/export-history/download/${taskId}`,
      {
        responseType: "blob"
      }
    );

    const blob = new Blob(
      [downloadResponse.data],
      { type: "text/csv" }
    );

    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "trekking_history.csv";

    document.body.appendChild(link);
    link.click();
    link.remove();

    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error(error.response?.data || error);
    alert("Unable to export trekking history.");
  } finally {
    exporting.value = false;
  }
};

onMounted(() => {
  loadBookings()
})
</script>