<script setup>
import { ref } from "vue";
import api from "../services/api";
import { useRouter } from "vue-router";

const router = useRouter();

const username = ref("");
const name = ref("");
const email = ref("");
const password = ref("");

const handleRegister = async () => {
    try {
        const response = await api.post("/register", {
            username: username.value,
            name: name.value,
            email: email.value,
            password: password.value,
        });

        console.log(response.data);
        alert("Registration successful! Please log in.");
        router.push("/login");
    } catch (error) {
        console.error(error.response.data);
        alert(error.response.data);
    }
};

</script>

<template>
    <div>
        <h1>Register</h1>

        <form @submit.prevent="handleRegister">

            <div>
                <label>Username</label><br>
                <input
                    type="text"
                    v-model="username"
                    placeholder="Enter username"
                >
            </div>

            <br>

            <div>
                <label>Full Name</label><br>
                <input
                    type="text"
                    v-model="name"
                    placeholder="Enter full name"
                >
            </div>

            <br>

            <div>
                <label>Email</label><br>
                <input
                    type="email"
                    v-model="email"
                    placeholder="Enter email"
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
                Register
            </button>

            <p>
                Already have an account?
                <router-link to="/login">
                    Login
                </router-link>
            </p>

        </form>
    </div>
</template>

<style scoped>
</style>