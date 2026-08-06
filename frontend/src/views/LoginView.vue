<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const router = useRouter();

const login = ref("");
const password = ref("");
const error = ref("");

const handleLogin = async () => {
  error.value = "";

  try {
    const response = await api.post("/login", {
      login: login.value,
      password: password.value,
    });

    localStorage.setItem("token", response.data.access_token);
    localStorage.setItem("role", response.data.role);

    if (response.data.role === "admin") {
      router.push("/admin/dashboard");
    } else if (response.data.role === "staff") {
      router.push("/staff/dashboard");
    } else {
      router.push("/trekker/dashboard");
    }
  } catch (err) {
    error.value =
      err.response?.data?.message || "Invalid credentials"

      setTimeout(() => {
        error.value = ""
      }, 3000)
    }
}
</script>

<template>
  <div class="container-fluid bg-light min-vh-100 d-flex justify-content-center align-items-center">

    <div style="width: 450px;">

      <!-- Heading -->
      <div class="text-center mb-4">

        <h1 class="fw-bold display-6 mb-2">
          Welcome Back
        </h1>

        <p class="text-secondary mb-0">
          Sign in to your Trekkify account.
        </p>

      </div>

      <!-- Login Card -->
      <div class="card border-0 shadow rounded-4 p-5">

        <div
          v-if="error"
          class="alert alert-danger"
        >
          {{ error }}
        </div>

        <form @submit.prevent="handleLogin">

          <div class="mb-3">

            <label class="form-label">
              Username or Email
            </label>

            <input
              v-model="login"
              type="text"
              class="form-control py-2"
              placeholder="Enter your username or email"
              required
            >

          </div>

          <div class="mb-4">

            <label class="form-label">
              Password
            </label>

            <input
              v-model="password"
              type="password"
              class="form-control py-2"
              placeholder="Enter your password"
              required
            >

          </div>

          <button
            type="submit"
            class="btn btn-primary w-100 py-2 fw-semibold"
          >
            Login
          </button>

        </form>

        <hr class="my-4">

        <div class="text-center">

          <span class="text-muted">
            Don't have an account?
          </span>

          <RouterLink
            to="/register"
            class="text-decoration-none fw-semibold ms-1"
          >
            Register
          </RouterLink>

        </div>

      </div>

    </div>

  </div>
</template>