<template>
  <AppLayout title="Manage Trek">

    <!-- Success Alert -->
    <div
      v-if="successMessage"
      class="alert alert-success alert-dismissible fade show"
    >
      {{ successMessage }}
    </div>

    <!-- Trek Details -->
    <div class="card shadow-sm border-0 rounded-4 mb-4">

      <div class="card-header bg-white">
        <h5 class="mb-0">Trek Details</h5>
      </div>

      <div class="card-body">

        <!-- Trek Information -->
        <div class="row g-4 mb-4">

          <div class="col-md-6">

            <strong>Name</strong>

            <p class="text-secondary mb-0">
              {{ trek.trek_name }}
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

            <strong>Registered Participants</strong>

            <p class="text-secondary mb-0">
              {{ trek.participants }}
            </p>

          </div>

        </div>

        <hr>

        <!-- Editable Fields -->
        <div class="row g-4 align-items-end">

          <div class="col-md-4">

            <label class="form-label fw-semibold">
              Available Slots
            </label>

            <input
              type="number"
              min="0"
              class="form-control"
              v-model="trek.available_slots"
            >

          </div>

          <div class="col-md-4">

            <label class="form-label fw-semibold">
              Trek Status
            </label>

            <select
              class="form-select"
              v-model="trek.status"
            >
              <option value="Open">Open</option>
              <option value="Closed">Closed</option>
              <option value="Started">Started</option>
              <option value="Completed">Completed</option>
            </select>

          </div>

          <div class="col-md-4">

            <button
              class="btn btn-primary w-100"
              @click="openConfirmModal"
            >
              <i class="bi bi-save me-2"></i>
              Save Changes
            </button>

          </div>

        </div>

      </div>

    </div>

<!-- Participants -->

<div class="card shadow-sm border-0 rounded-4">

  <div
    class="card-header bg-white d-flex justify-content-between align-items-center"
  >

    <h5 class="mb-0">
      Registered Participants
    </h5>

    <span class="badge bg-primary">
      {{ participants.length }}
    </span>

  </div>

  <div class="card-body">

    <table class="table table-hover align-middle">

      <thead>

        <tr>

        <th class="w-25">Name</th>
        <th class="w-35">Email</th>
        <th class="w-20">Booking Status</th>
        <th class="w-20">Booking Date</th>

        </tr>

      </thead>

      <tbody>

        <tr
          v-for="participant in participants"
          :key="participant.booking_id"
        >

          <td>
            {{ participant.name }}
          </td>

          <td>
            {{ participant.email }}
          </td>

            <td>

              <select
                class="form-select form-select-sm w-100"
                v-model="participant.booking_status"
              >
                <option value="Booked">Booked</option>
                <option value="Cancelled">Cancelled</option>
                <option value="Completed">Completed</option>
              </select>

            </td>

          <td>
            {{ formatDate(participant.booking_date) }}
          </td>

        </tr>

        <tr v-if="participants.length === 0">

          <td
            colspan="4"
            class="text-center text-muted py-5"
          >

            <i class="bi bi-people fs-2 d-block mb-2"></i>

            No participants have registered for this trek yet.

          </td>

        </tr>

      </tbody>

    </table>

    <div
      v-if="participants.length"
      class="d-flex justify-content-end mt-4"
    >

      <button
        class="btn btn-primary px-4"
        @click="updateBookingStatus"
      >

        <i class="bi bi-check-circle me-2"></i>

        Update Booking Status

      </button>

    </div>

  </div>

</div>

    <!-- Confirmation Modal -->

    <div
      class="modal fade"
      tabindex="-1"
      ref="confirmModal"
    >

        <div
          class="modal-dialog"
          style="margin-top: 80px;"
        >

        <div class="modal-content">

          <div class="modal-header">

            <h5 class="modal-title">
              Confirm Changes
            </h5>

            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>

          </div>

          <div class="modal-body">

            <p class="mb-0">
              Are you sure you want to save these changes?
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
              @click="updateTrek"
              :disabled="loading"
            >

              <span
                v-if="loading"
                class="spinner-border spinner-border-sm me-2"
              ></span>

              {{ loading ? "Saving..." : "Confirm" }}

            </button>

          </div>

        </div>

      </div>

    </div>

  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute } from "vue-router"
import { Modal } from "bootstrap"
import AppLayout from "../../components/AppLayout.vue"
import api from "../../services/api"

const route = useRoute()

const trek = ref({})
const participants = ref([])

const loading = ref(false)
const successMessage = ref("")

const confirmModal = ref(null)
let modal = null

const originalSlots = ref(0)
const originalStatus = ref("")

const hasChanges = computed(() => {
  return (
    Number(trek.value.available_slots) !== Number(originalSlots.value) ||
    trek.value.status !== originalStatus.value
  )
})

const loadTrek = async () => {
  try {
    const response = await api.get(`/staff/treks/${route.params.id}`)

    trek.value = response.data
    originalSlots.value = response.data.available_slots
    originalStatus.value = response.data.status
  } catch (error) {
    console.error(error.response?.data || error)
  }
}

const loadParticipants = async () => {
  try {
    const response = await api.get(`/staff/treks/${route.params.id}/participants`)
    participants.value = response.data
  } catch (error) {
    console.error(error.response?.data || error)
  }
}

const openConfirmModal = () => {
  if (!hasChanges.value) return
  modal.show()
}

const updateTrek = async () => {
  loading.value = true

  try {
    await api.put(`/staff/treks/${route.params.id}`, {
      available_slots: trek.value.available_slots,
      status: trek.value.status,
    })

    modal.hide()

    await loadTrek()
    await loadParticipants()

    successMessage.value = "Trek updated successfully."

    setTimeout(() => {
      successMessage.value = ""
    }, 3000)

  } catch (error) {
    console.error(error.response?.data || error)
  } finally {
    loading.value = false
  }
}

const updateBookingStatus = async () => {
  try {

    await api.put("/staff/bookings", participants.value)

    successMessage.value = "Booking statuses updated successfully."

    setTimeout(() => {
      successMessage.value = ""
    }, 3000)

    await loadParticipants()

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

onMounted(async () => {
  modal = new Modal(confirmModal.value)
  await loadTrek()
  await loadParticipants()
})
</script>