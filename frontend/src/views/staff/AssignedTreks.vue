<template>
  <AppLayout title="My Treks">

    <div class="card shadow-sm border-0 rounded-4">

      <div class="card-header bg-white">
        <h5 class="mb-0">Assigned Treks</h5>
      </div>

      <div class="card-body">

        <table class="table table-hover align-middle">

          <thead>
            <tr>
              <th>Name</th>
              <th>Difficulty</th>
              <th>Duration</th>
              <th>Slots</th>
              <th>Status</th>
              <th>Participants</th>
              <th></th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="trek in treks"
              :key="trek.id"
            >

              <td>{{ trek.trek_name }}</td>

              <td>{{ trek.difficulty }}</td>

              <td>{{ trek.duration }} Days</td>

              <td>{{ trek.available_slots }}</td>

              <td>
                <span class="badge bg-success">
                  {{ trek.status }}
                </span>
              </td>

              <td>{{ trek.registered_users }}</td>

              <td>
                <button
                  class="btn btn-primary btn-sm"
                  @click="manageTrek(trek.id)"
                >
                  Manage
                </button>
              </td>

            </tr>

            <tr v-if="treks.length === 0">
              <td colspan="7" class="text-center text-muted py-4">
                No treks assigned.
              </td>
            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import AppLayout from "../../components/AppLayout.vue"
import api from "../../services/api"

const router = useRouter()

const treks = ref([])

const loadTreks = async () => {
  try {
    const response = await api.get("/staff/treks")
    treks.value = response.data
  } catch (error) {
    console.error(error.response?.data || error)
  }
}

const manageTrek = (id) => {
  router.push(`/staff/treks/${id}`)
}

onMounted(loadTreks)
</script>