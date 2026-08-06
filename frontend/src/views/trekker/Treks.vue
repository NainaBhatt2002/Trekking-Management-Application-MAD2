<template>
  <AppLayout title="Browse Treks">

    <div class="card shadow-sm border-0 rounded-4 mb-4">

      <div class="card-body">

        <div class="row g-3">

          <div class="col-lg-4">

            <SearchBar
              v-model="search"
              placeholder="Search Trek..."
            />

          </div>

          <div class="col-lg-3">

            <select
              class="form-select"
              v-model="difficulty"
            >
              <option value="">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Moderate">Moderate</option>
              <option value="Hard">Hard</option>
            </select>

          </div>

          <div class="col-lg-3">

            <input
              type="text"
              class="form-control"
              placeholder="Location"
              v-model="location"
            >

          </div>

          <div class="col-lg-2">

            <select
              class="form-select"
              v-model="duration"
            >
              <option value="">All Durations</option>

              <option
                v-for="day in durationOptions"
                :key="day"
                :value="day"
              >
                {{ day }} {{ day === 1 ? "Day" : "Days" }}
              </option>

            </select>

          </div>

        </div>

      </div>

    </div>

    <div
      v-if="treks.length"
      class="row g-4"
    >

      <div
        class="col-lg-4 col-md-6"
        v-for="trek in treks"
        :key="trek.id"
      >

        <TrekCard
          :trek="trek"
        />

      </div>

    </div>

    <div
      v-else
      class="card shadow-sm border-0 rounded-4"
    >

      <div class="card-body text-center py-5">

        <i class="bi bi-search fs-1 text-secondary"></i>

        <h5 class="mt-3">
          No Treks Found
        </h5>

        <p class="text-secondary mb-0">
          Try changing your search or filter options.
        </p>

      </div>

    </div>

  </AppLayout>
</template>

<script setup>
import { ref, watch, onMounted } from "vue"
import AppLayout from "../../components/AppLayout.vue"
import SearchBar from "../../components/SearchBar.vue"
import TrekCard from "../../components/TrekCard.vue"
import api from "../../services/api"

const treks = ref([])

const search = ref("")
const difficulty = ref("")
const location = ref("")
const duration = ref("")

const loadTreks = async () => {
  try {
    const response = await api.get("/trekker/treks", {
      params: {
        search: search.value,
        difficulty: difficulty.value,
        location: location.value,
        duration: duration.value,
      },
    })

    treks.value = response.data
    generateDurationOptions()

  } catch (error) {
    console.error(error.response?.data || error)
  }
}

const durationOptions = ref([])

const generateDurationOptions = () => {
  const durations = [...new Set(
    treks.value.map(trek => trek.duration)
  )]

  durationOptions.value = durations.sort((a, b) => a - b)
}

watch(
  [search, difficulty, location, duration],
  loadTreks
)

onMounted(() => {
  loadTreks()
})
</script>