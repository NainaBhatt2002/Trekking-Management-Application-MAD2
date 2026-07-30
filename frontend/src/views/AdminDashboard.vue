<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const router = useRouter();

const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");

    router.push("/login");
};

onMounted(async () => {
    try {
        const response = await api.get("/profile");
        console.log(response.data);
    } catch (error) {
        console.error(error.response?.data || error);
    }
});

</script>

<template>
    <div>
        <h1>Admin Dashboard</h1>

        <button @click="logout">
            Logout
        </button>
    </div>
</template>