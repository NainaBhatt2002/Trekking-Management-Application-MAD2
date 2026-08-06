<template>
  <div class="card shadow-sm border-0 rounded-4 h-100">

    <div class="card-body d-flex flex-column">

      <div class="d-flex justify-content-between align-items-center mb-3">

        <h5 class="fw-bold mb-0">
          <i class="bi bi-tree-fill text-success me-2"></i>
          {{ trek.trek_name }}
        </h5>

        <span
          class="badge"
          :class="{
            'bg-success': trek.status === 'Open',
            'bg-danger': trek.status === 'Closed',
            'bg-secondary': trek.status === 'Completed'
          }"
        >
          {{ trek.status }}
        </span>

      </div>

      <div class="mb-2">

        <strong>Difficulty</strong>

        <span
          class="badge ms-2"
          :class="{
            'bg-success': trek.difficulty === 'Easy',
            'bg-warning text-dark': trek.difficulty === 'Moderate',
            'bg-danger': trek.difficulty === 'Hard'
          }"
        >
          {{ trek.difficulty }}
        </span>

      </div>

      <p class="mb-2">
        <strong>Duration:</strong>
        {{ trek.duration }} Days
      </p>

      <p class="mb-4">
        <strong>Available Slots:</strong>
        {{ trek.available_slots }}
      </p>

      <button
        class="btn btn-primary mt-auto"
        @click="viewTrek"
      >
        <i class="bi bi-eye me-2"></i>
        View Details
      </button>

    </div>

  </div>
</template>

<script setup>
import { useRouter } from "vue-router"

const props = defineProps({
  trek: {
    type: Object,
    required: true,
  },
})

const router = useRouter()

const viewTrek = () => {
  router.push(`/trekker/treks/${props.trek.id}`)
}
</script>