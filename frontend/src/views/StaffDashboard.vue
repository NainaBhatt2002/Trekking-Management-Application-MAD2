<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");

    router.push("/login");
};
</script>

<template>
    <div>
        <h1>Staff Dashboard</h1>

        <button @click="logout">
            Logout
        </button>
    </div>
</template>