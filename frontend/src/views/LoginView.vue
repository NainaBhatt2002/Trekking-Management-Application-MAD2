<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const login = ref("");
const password = ref("");
const router = useRouter();

const handleLogin = async () => {
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

    } catch (error) {
        console.error(error.response.data);
    }
};

</script>

<template>
    <div>
        <h1>Login</h1>

        <form @submit.prevent="handleLogin">

            <div>
                <label>Username or Email</label><br>
                <input
                    type="text"
                    v-model="login"
                    placeholder="Enter username or email"
                >
            </div>

            <br>

            <div>
                <label>Password</label><br>
                <input
                    type="password"
                    v-model="password"
                    placeholder="Enter password"
                >
            </div>

            <br>

            <button type="submit">
                Login
            </button>

            <p>
                Don't have an account?
                <router-link to="/register">
                    Register
                </router-link>
            </p>

        </form>
    </div>
</template>

<style scoped>
</style>