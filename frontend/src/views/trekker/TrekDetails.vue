<template>
  <AppLayout title="Trek Details">

    <div
      v-if="successMessage"
      class="alert alert-success alert-dismissible fade show"
    >
      {{ successMessage }}
    </div>

    <div
      v-if="errorMessage"
      class="alert alert-danger alert-dismissible fade show"
    >
      {{ errorMessage }}
    </div>

    <div class="card shadow-sm border-0 rounded-4">

      <div class="card-header bg-white">
        <h4 class="mb-0">
          {{ trek.trek_name }}
        </h4>
      </div>

      <div class="card-body">

        <div class="row g-4">

          <div class="col-md-6">

            <strong>Location</strong>

            <p class="text-secondary mb-0">
              {{ trek.location }}
            </p>

          </div>

          <div class="col-md-6">

            <strong>Difficulty</strong>

            <p class="mb-0">

              <span
                class="badge"
                :class="{
                  'bg-success': trek.difficulty === 'Easy',
                  'bg-warning text-dark': trek.difficulty === 'Moderate',
                  'bg-danger': trek.difficulty === 'Hard'
                }"
              >
                {{ trek.difficulty }}
              </span>

            </p>

          </div>

          <div class="col-md-6">

            <strong>Duration</strong>

            <p class="text-secondary mb-0">
              {{ trek.duration }} Days
            </p>

          </div>

          <div class="col-md-6">

            <strong>Available Slots</strong>

            <p class="text-secondary mb-0">
              {{ trek.available_slots }}
            </p>

          </div>

          <div class="col-md-6">

            <strong>Status</strong>

            <p>

              <span
                class="badge"
                :class="trek.status === 'Open'
                  ? 'bg-success'
                  : 'bg-danger'"
              >
                {{ trek.status }}
              </span>

            </p>

          </div>

        </div>

        <hr>

        <div class="text-end">

        <button
        class="btn btn-primary"
        :disabled="trek.available_slots <= 0 || trek.status !== 'Open' || alreadyBooked"
        @click="openBookingModal"
        >
            <i class="bi bi-journal-check me-2"></i>
            {{ alreadyBooked ? 'Already Booked' : 'Book Trek' }}
        </button>

        </div>

      </div>

    </div>

    <!-- Booking Modal -->

    <div
      class="modal fade"
      tabindex="-1"
      ref="bookingModal"
    >

      <div
        class="modal-dialog"
        style="margin-top:80px;"
      >

        <div class="modal-content">

          <div class="modal-header">

            <h5 class="modal-title">
              Confirm Booking
            </h5>

            <button
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>

          </div>

          <div class="modal-body">

            <p>

              Book

              <strong>
                {{ trek.trek_name }}
              </strong>

              ?

            </p>

          </div>

          <div class="modal-footer">

            <button
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Cancel
            </button>

            <button
              class="btn btn-primary"
              @click="bookTrek"
              :disabled="loading"
            >

              <span
                v-if="loading"
                class="spinner-border spinner-border-sm me-2"
              ></span>

              {{ loading ? "Booking..." : "Confirm Booking" }}

            </button>

          </div>

        </div>

      </div>

    </div>

  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"
import { Modal } from "bootstrap"
import AppLayout from "../../components/AppLayout.vue"
import api from "../../services/api"

const route = useRoute()

const trek = ref({})

const loading = ref(false)

const alreadyBooked = ref(false)

const successMessage = ref("")
const errorMessage = ref("")

const bookingModal = ref(null)

let modal = null

const loadTrek = async () => {
  try {

    const response = await api.get(`/trekker/treks/${route.params.id}`)

    trek.value = response.data

    alreadyBooked.value = response.data.is_booked || false

  } catch (error) {
    console.error(error.response?.data || error)
  }
}

const openBookingModal = () => {
  modal.show()
}

const bookTrek = async () => {
  loading.value = true

  try {

    const response = await api.post(`/trekker/bookings/${route.params.id}`)

    successMessage.value = response.data.message

    alreadyBooked.value = true

    errorMessage.value = ""

    modal.hide()

    await loadTrek()

    setTimeout(() => {
      successMessage.value = ""
    }, 3000)

  } catch (error) {

    errorMessage.value =
      error.response?.data?.message || "Booking failed"

    setTimeout(() => {
      errorMessage.value = ""
    }, 3000)

  } finally {

    loading.value = false

  }
}

onMounted(async () => {

  modal = new Modal(bookingModal.value)

  await loadTrek()

})
</script>