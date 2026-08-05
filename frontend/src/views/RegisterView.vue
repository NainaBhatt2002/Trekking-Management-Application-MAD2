<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const router = useRouter();

const form = ref({
  username: "",
  name: "",
  email: "",
  password: "",
});

const error = ref("");
const success = ref("");

const register = async () => {
  error.value = "";
  success.value = "";

  try {
    const response = await api.post("/register", form.value);

    success.value = response.data;

    setTimeout(() => {
      router.push("/login");
    }, 1500);

  } catch (err) {
    error.value = err.response?.data || "Registration failed";
  }
};
</script>

<template>
  <div class="container-fluid bg-light min-vh-100 d-flex justify-content-center align-items-center">

    <div style="width: 450px;">

      <!-- Heading -->
      <div class="text-center mb-4">

        <h1 class="fw-bold display-6 mb-2">
          Join Trekkify
        </h1>

        <p class="text-secondary mb-0">
          Create your Trekkify account.
        </p>

      </div>

      <div class="card border-0 shadow rounded-4 p-5">

        <div
          v-if="error"
          class="alert alert-danger"
        >
          {{ error }}
        </div>

        <div
          v-if="success"
          class="alert alert-success"
        >
          {{ success }}
        </div>

        <form @submit.prevent="register">

          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input
              v-model="form.name"
              type="text"
              class="form-control py-2"
              placeholder="Enter your full name"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Username</label>
            <input
              v-model="form.username"
              type="text"
              class="form-control py-2"
              placeholder="Choose a username"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input
              v-model="form.email"
              type="email"
              class="form-control py-2"
              placeholder="Enter your email"
              required
            >
          </div>

          <div class="mb-4">
            <label class="form-label">Password</label>
            <input
              v-model="form.password"
              type="password"
              class="form-control py-2"
              placeholder="Create a password"
              required
            >
          </div>

          <button
            type="submit"
            class="btn btn-primary w-100 py-2 fw-semibold"
          >
            Create Account
          </button>

        </form>

        <hr class="my-4">

        <div class="text-center">

          <span class="text-muted">
            Already have an account?
          </span>

          <RouterLink
            to="/login"
            class="text-decoration-none fw-semibold ms-1"
          >
            Login
          </RouterLink>

        </div>

      </div>

    </div>

  </div>
</template>