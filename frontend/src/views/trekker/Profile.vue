<template>

  <AppLayout title="My Profile">

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
        <h5 class="mb-0">
          My Profile
        </h5>
      </div>

      <div class="card-body">

        <div class="row g-4">

          <div class="col-md-6">

            <label class="form-label fw-semibold">
              Username
            </label>

            <input
              type="text"
              class="form-control"
              v-model="profile.username"
              readonly
            >

          </div>

          <div class="col-md-6">

            <label class="form-label fw-semibold">
              Full Name
            </label>

            <input
              type="text"
              class="form-control"
              v-model="profile.name"
            >

          </div>

          <div class="col-md-6">

            <label class="form-label fw-semibold">
              Email
            </label>

            <input
              type="email"
              class="form-control"
              v-model="profile.email"
            >

          </div>

        <div class="col-md-6">
            <label class="form-label fw-semibold">
                Phone Number
            </label>

            <input
                type="tel"
                class="form-control"
                v-model="profile.phone"
                placeholder="Enter Phone Number"
            >
        </div>

        <div class="col-md-6">
            <label class="form-label fw-semibold">
                Gender
            </label>

            <select
                class="form-select"
                v-model="profile.gender"
            >
                <option value="">Select Gender</option>
                <option>Male</option>
                <option>Female</option>
                <option>Other</option>
            </select>
        </div>

        <div class="col-md-6">
            <label class="form-label fw-semibold">
                Age
            </label>

            <input
                type="number"
                class="form-control"
                min="10"
                max="80"
                v-model="profile.age"
            >
        </div>

        <div class="col-md-6">
            <label class="form-label fw-semibold">
                Blood Group
            </label>

            <select
                class="form-select"
                v-model="profile.blood_group"
            >
                <option value="">Select Blood Group</option>
                <option>A+</option>
                <option>A-</option>
                <option>B+</option>
                <option>B-</option>
                <option>AB+</option>
                <option>AB-</option>
                <option>O+</option>
                <option>O-</option>
            </select>
        </div>

        <div class="col-md-6">
            <label class="form-label fw-semibold">
                Emergency Contact
            </label>

            <input
                type="tel"
                class="form-control"
                v-model="profile.emergency_contact"
                placeholder="Enter Emergency Contact Number"
            >
        </div>

        <div class="col-12">
            <label class="form-label fw-semibold">
                Address
            </label>

            <textarea
                class="form-control"
                v-model="profile.address"
                rows="3"
                placeholder="Enter Address"
            ></textarea>
          </div>

          <div class="col-md-6">

            <label class="form-label fw-semibold">
              Role
            </label>

            <input
              type="text"
              class="form-control"
              value="Trekker"
              readonly
            >

          </div>

        </div>

        <hr>

        <div class="text-end">

          <button
            class="btn btn-primary"
            @click="updateProfile"
            :disabled="loading"
          >

            <span
              v-if="loading"
              class="spinner-border spinner-border-sm me-2"
            ></span>

            {{ loading ? "Saving..." : "Save Changes" }}

          </button>

        </div>

      </div>

    </div>

  </AppLayout>

</template>

<script setup>
import { ref, onMounted } from "vue"
import AppLayout from "../../components/AppLayout.vue"
import api from "../../services/api"

const profile = ref({
  username: "",
  name: "",
  email: "",
  phone: "",
  gender: "",
  age: null,
  blood_group: "",
  emergency_contact: "",
  address: ""
})

const loading = ref(false)
const successMessage = ref("")
const errorMessage = ref("")

const loadProfile = async () => {
  try {
    const response = await api.get("/trekker/profile")
    profile.value = response.data
  } catch (error) {
    console.error(error.response?.data || error)
  }
}

const updateProfile = async () => {
  errorMessage.value = ""
  successMessage.value = ""

  if (!profile.value.name.trim()) {
    errorMessage.value = "Full name is required."
    return
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!emailRegex.test(profile.value.email.trim())) {
    errorMessage.value = "Please enter a valid email address."
    return
  }

  const phoneRegex = /^[6-9]\d{9}$/

  if (
    profile.value.phone &&
    !phoneRegex.test(profile.value.phone)
  ) {
    errorMessage.value = "Please enter a valid 10-digit phone number."
    return
  }

  if (
    profile.value.emergency_contact &&
    !phoneRegex.test(profile.value.emergency_contact)
  ) {
    errorMessage.value = "Please enter a valid emergency contact number."
    return
  }

  if (
    profile.value.age &&
    (profile.value.age < 18 || profile.value.age > 80)
  ) {
    errorMessage.value = "Age must be between 18 and 80."
    return
  }

  loading.value = true

  try {
    const response = await api.put(
      "/trekker/profile",
      profile.value
    )

    successMessage.value = response.data.message

    setTimeout(() => {
      successMessage.value = ""
    }, 3000)

  } catch (error) {
    errorMessage.value =
      error.response?.data?.message || "Unable to update profile."

    setTimeout(() => {
      errorMessage.value = ""
    }, 3000)

  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>