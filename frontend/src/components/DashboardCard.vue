<template>
  <div class="col-md-6 col-lg-3">
    <div class="card border-0 shadow-sm rounded-4 h-100">
      <div class="card-body d-flex justify-content-between align-items-center p-4">
        <div>
          <span class="text-secondary fw-semibold small text-uppercase">{{ title }}</span>
          <h2 class="fw-bold mt-2 mb-0 text-dark">{{ value }}</h2>
        </div>

        <div
          class="bg-primary bg-opacity-10 text-primary rounded-circle d-flex justify-content-center align-items-center"
          style="width: 60px; height: 60px;"
        >
          <i :class="icon" class="fs-2 text-primary"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [Number, String],
    required: true,
  },
  icon: {
    type: String,
    required: true,
  },
});
</script>
