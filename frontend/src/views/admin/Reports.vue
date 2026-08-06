<template>

  <AppLayout title="Reports">

    <div v-if="report">

      <div class="row g-4 mb-4">

        <div class="col-md-3">
          <div class="card shadow-sm border-0 text-center">
            <div class="card-body">
              <h6>Total Treks</h6>
              <h2>{{ report.summary.total_treks }}</h2>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card shadow-sm border-0 text-center">
            <div class="card-body">
              <h6>Total Users</h6>
              <h2>{{ report.summary.total_users }}</h2>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card shadow-sm border-0 text-center">
            <div class="card-body">
              <h6>Total Staff</h6>
              <h2>{{ report.summary.total_staff }}</h2>
            </div>
          </div>
        </div>

        <div class="col-md-3">
              <div class="card shadow-sm border-0">
            <div class="card-body d-flex flex-column justify-content-center align-items-center">
                <h6 class="mb-2 text-center">Total Bookings</h6>
                <h2 class="mb-0">{{ report.summary.total_bookings }}</h2>
            </div>
        </div>
        </div>

      </div>

    </div>

<div class="row g-4 mb-4">

  <!-- Trek Difficulty -->

  <div class="col-lg-6">

    <div class="card shadow-sm border-0 h-100">

      <div class="card-body">

        <h5 class="mb-3">
          Trek Difficulty Distribution
        </h5>

        <div
          class="d-flex justify-content-center align-items-center"
          style="height:300px;"
        >
          <Pie
            :data="difficultyData"
            :options="chartOptions"
          />
        </div>

      </div>

    </div>

  </div>

  <!-- Trek Status -->

  <div class="col-lg-6">

    <div class="card shadow-sm border-0 h-100">

      <div class="card-body">

        <h5 class="mb-3">
          Trek Status
        </h5>

        <div
          class="d-flex justify-content-center align-items-center"
          style="height:300px;"
        >
          <Doughnut
            :data="trekStatusData"
            :options="chartOptions"
          />
        </div>

      </div>

    </div>

  </div>

</div>

<!-- User Status -->

<div class="row g-4 mb-4">

  <div class="col-lg-6">

    <div class="card shadow-sm border-0 h-100">

      <div class="card-body">

        <h5 class="mb-3">
          User Status
        </h5>

        <div
          class="d-flex justify-content-center align-items-center"
          style="height:300px;"
        >
          <Bar
            :data="userStatusData"
            :options="chartOptions"
          />
        </div>

      </div>

    </div>

  </div>

  <!-- Staff Status -->

  <div class="col-lg-6">

    <div class="card shadow-sm border-0 h-100">

      <div class="card-body">

        <h5 class="mb-3">
          Staff Status
        </h5>

        <div
          class="d-flex justify-content-center align-items-center"
          style="height:300px;"
        >
          <Bar
            :data="staffStatusData"
            :options="chartOptions"
          />
        </div>

      </div>

    </div>

  </div>

</div>

<!-- Booking Status -->

<div class="row g-4 mb-4">

  <div class="col-lg-6">

    <div class="card shadow-sm border-0 h-100">

      <div class="card-body">

        <h5 class="mb-3">
          Booking Status
        </h5>

        <div
          v-if="report?.summary.total_bookings === 0"
          class="d-flex justify-content-center align-items-center"
          style="height:300px;"
        >
          <p class="text-muted mb-0">
            No booking data available yet.
          </p>
        </div>

        <div
          v-else
          class="d-flex justify-content-center align-items-center"
          style="height:300px;"
        >
          <Pie
            :data="bookingStatusData"
            :options="chartOptions"
          />
        </div>

      </div>

    </div>

  </div>

  <!-- Payment Status -->

  <div class="col-lg-6">

    <div class="card shadow-sm border-0 h-100">

      <div class="card-body">

        <h5 class="mb-3">
          Payment Status
        </h5>

        <div
          v-if="report?.summary.total_bookings === 0"
          class="d-flex justify-content-center align-items-center"
          style="height:300px;"
        >
          <p class="text-muted mb-0">
            No payment data available yet.
          </p>
        </div>

        <div
          v-else
          class="d-flex justify-content-center align-items-center"
          style="height:300px;"
        >
          <Doughnut
            :data="paymentStatusData"
            :options="chartOptions"
          />
        </div>

      </div>

    </div>

  </div>

</div>

  </AppLayout>

</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import { Pie, Doughnut, Bar } from "vue-chartjs";
import api from "../../services/api";
import AppLayout from "../../components/AppLayout.vue";

ChartJS.register(
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

const report = ref(null);

const loadReports = async () => {
  try {
    const response = await api.get("/admin/reports");
    report.value = response.data;
  } catch (error) {
    console.error(error.response?.data || error);
  }
};

const difficultyData = computed(() => ({
  labels: ["Easy", "Moderate", "Hard"],
  datasets: [
    {
      data: [
        report.value?.difficulty.Easy || 0,
        report.value?.difficulty.Moderate || 0,
        report.value?.difficulty.Hard || 0,
      ],
      backgroundColor: [
        "#4CAF50",
        "#FFC107",
        "#F44336",
      ],
    },
  ],
}));

const trekStatusData = computed(() => ({
  labels: ["Open", "Closed"],
  datasets: [
    {
      data: [
        report.value?.trek_status.Open || 0,
        report.value?.trek_status.Closed || 0,
      ],
      backgroundColor: [
        "#198754",
        "#dc3545",
      ],
    },
  ],
}));

const userStatusData = computed(() => ({
  labels: ["Active", "Inactive"],
  datasets: [
    {
      label: "Users",
      data: [
        report.value?.users.Active || 0,
        report.value?.users.Inactive || 0,
      ],
      backgroundColor: [
        "#198754",
        "#dc3545",
      ],
    },
  ],
}));

const staffStatusData = computed(() => ({
  labels: ["Active", "Inactive"],
  datasets: [
    {
      label: "Staff",
      data: [
        report.value?.staff.Active || 0,
        report.value?.staff.Inactive || 0,
      ],
      backgroundColor: [
        "#198754",
        "#dc3545",
      ],
    },
  ],
}));

const bookingStatusData = computed(() => ({
  labels: ["Pending", "Confirmed", "Cancelled"],
  datasets: [
    {
      data: [
        report.value?.booking_status.Pending || 0,
        report.value?.booking_status.Confirmed || 0,
        report.value?.booking_status.Cancelled || 0,
      ],
      backgroundColor: [
        "#ffc107",
        "#198754",
        "#dc3545",
      ],
    },
  ],
}));

const paymentStatusData = computed(() => ({
  labels: ["Paid", "Pending"],
  datasets: [
    {
      data: [
        report.value?.payment_status.Paid || 0,
        report.value?.payment_status.Pending || 0,
      ],
      backgroundColor: [
        "#198754",
        "#ffc107",
      ],
    },
  ],
}));

onMounted(loadReports);
</script>