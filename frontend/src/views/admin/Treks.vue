<template>
  <AppLayout title="Treks">

    <div class="d-flex justify-content-between align-items-center mb-4">

      <h3 class="fw-bold mb-0">
        Manage all Treks
      </h3>

      <button
        class="btn btn-primary"
        @click="openModal"
      >
        <i class="bi bi-plus-lg me-2"></i>
        Add Trek
      </button>

    </div>

  <SearchBar
    v-model="search"
    class="mb-4"
    placeholder="Search by Trek ID or Name"
  />

    <div class="card border-0 shadow-sm rounded-4">

      <div class="card-body">

        <table class="table table-hover align-middle">

        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Difficulty</th>
            <th>Duration</th>
            <th>Trek Date</th>
            <th>Slots</th>
            <th>Staff</th>
            <th>Status</th>
            <th class="text-center">Actions</th>
          </tr>
        </thead>

          <tbody v-if="filteredTreks.length">

            <tr
              v-for="trek in filteredTreks"
              :key="trek.id"
            >

              <td>{{ trek.id }}</td>
              <td>{{ trek.trek_name }}</td>
              <td>{{ trek.difficulty }}</td>
              <td>{{ trek.duration }} Days</td>
              <td>{{ trek.trek_date }}</td>
              <td>{{ trek.available_slots }}</td>
              <td>{{ trek.staff }}</td>

              <td>

                <span
                  class="badge"
                  :class="trek.status === 'Open' ? 'bg-success' : 'bg-danger'"
                >
                  {{ trek.status }}
                </span>

              </td>

              <td class="text-center">

                <button
                  class="btn btn-sm btn-outline-primary me-2"
                  @click="editTrek(trek)"
                >
                  <i class="bi bi-pencil"></i>
                </button>

                  <button
                    class="btn btn-sm btn-outline-danger"
                    @click="openDeleteModal(trek)"
                  >
                  <i class="bi bi-trash"></i>
                </button>

              </td>

            </tr>

          </tbody>

          <tbody v-else>

            <tr>

              <td
                colspan="8"
                class="text-center text-muted py-5"
              >
                No treks found.
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

    <!-- Add Trek Pop up -->

    <div
      v-if="showModal"
      class="modal fade show"
      style="display:block;background:rgba(0,0,0,.5);"
    >

      <div class="modal-dialog modal-lg">

        <div class="modal-content">

          <div class="modal-header">

              <h5 class="modal-title">
                {{ isEditing ? "Edit Trek" : "Add Trek" }}
              </h5>

            <button
              type="button"
              class="btn-close"
              @click="closeModal"
            ></button>

          </div>

          <div class="modal-body">

            <div class="row">

              <div class="col-md-6 mb-3">

                <label class="form-label">
                  Trek Name <span class="text-danger">*</span>
                </label>

                <input
                  v-model="form.trek_name"
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': formErrors.trek_name }"
                  required
                >
                <div class="invalid-feedback">{{ formErrors.trek_name }}</div>

              </div>

                <div class="col-md-6 mb-3">

                  <label class="form-label">
                    Location <span class="text-danger">*</span>
                  </label>

                  <input
                    v-model="form.location"
                    type="text"
                    class="form-control"
                    :class="{ 'is-invalid': formErrors.location }"
                    placeholder="Enter Trek Location"
                    required
                  >
                  <div class="invalid-feedback">{{ formErrors.location }}</div>

                </div>

              <div class="col-md-6 mb-3">

                <label class="form-label">
                  Difficulty
                </label>

                <select
                  v-model="form.difficulty"
                  class="form-select"
                >
                  <option>Easy</option>
                  <option>Moderate</option>
                  <option>Hard</option>
                </select>

              </div>

              <div class="col-md-6 mb-3">

                <label class="form-label">
                  Duration (Days) <span class="text-danger">*</span>
                </label>

                <input
                  v-model="form.duration"
                  type="number"
                  class="form-control"
                  :class="{ 'is-invalid': formErrors.duration }"
                  min="1"
                  required
                >
                <div class="invalid-feedback">{{ formErrors.duration }}</div>

              </div>

              <div class="col-md-6 mb-3">
              <label class="form-label">
                Trek Date <span class="text-danger">*</span>
              </label>
              <input
                v-model="form.trek_date"
                type="date"
                class="form-control"
                :class="{ 'is-invalid': formErrors.trek_date }"
                required
              >
              <div class="invalid-feedback">{{ formErrors.trek_date }}</div>
            </div>

              <div class="col-md-6 mb-3">

                <label class="form-label">
                  Available Slots <span class="text-danger">*</span>
                </label>

                <input
                  v-model="form.available_slots"
                  type="number"
                  class="form-control"
                  :class="{ 'is-invalid': formErrors.available_slots }"
                  min="0"
                  required
                >
                <div class="invalid-feedback">{{ formErrors.available_slots }}</div>

              </div>

              <div class="col-md-6 mb-3">

                <label class="form-label">
                  Assign Staff <span class="text-danger">*</span>
                </label>

                <select
                  v-model="form.staff_id"
                  class="form-select"
                  :class="{ 'is-invalid': formErrors.staff_id }"
                  required
                >

                  <option
                    disabled
                    value=""
                  >
                    Select Staff
                  </option>

                  <option
                    v-for="staff in staffList"
                    :key="staff.id"
                    :value="staff.id"
                  >
                    {{ staff.name }}
                  </option>

                </select>
                <div class="invalid-feedback">{{ formErrors.staff_id }}</div>

              </div>

              <div class="col-md-6 mb-3">

                <label class="form-label">
                  Status
                </label>

                <select
                  v-model="form.status"
                  class="form-select"
                >
                  <option>Open</option>
                  <option>Closed</option>
                </select>

              </div>

            </div>

          </div>

          <div class="modal-footer">

            <button
              type="button"
              class="btn btn-secondary"
              @click="closeModal"
            >
              Cancel
            </button>

              <button
                type="button"
                class="btn btn-primary"
                @click="isEditing ? updateTrek() : createTrek()"
              >
                {{ isEditing ? "Update Trek" : "Create Trek" }}
              </button>

          </div>

        </div>

      </div>

    </div>


      <div
        v-if="showDeleteModal"
        class="modal fade show"
        style="display:block;background:rgba(0,0,0,.5);"
      >

        <div class="modal-dialog">

          <div class="modal-content">

            <div class="modal-header">

              <h5 class="modal-title">
                Delete Trek
              </h5>

              <button
                class="btn-close"
                @click="closeDeleteModal"
              ></button>

            </div>

            <div class="modal-body">

              <p>
                Are you sure you want to delete
                <strong>{{ selectedTrek?.trek_name }}</strong>?
              </p>

            </div>

            <div class="modal-footer">

              <button
                class="btn btn-secondary"
                @click="closeDeleteModal"
              >
                Cancel
              </button>

              <button
                class="btn btn-danger"
                @click="deleteTrek"
              >
                Delete
              </button>

            </div>

          </div>

        </div>

      </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../../services/api";
import AppLayout from "../../components/AppLayout.vue";
import SearchBar from "../../components/SearchBar.vue";

const treks = ref([]);
const staffList = ref([]);
const search = ref("");
const showModal = ref(false);
const isEditing = ref(false);
const editingId = ref(null);
const showDeleteModal = ref(false);
const selectedTrek = ref(null);

const formErrors = ref({});

const form = ref({
  trek_name: "",
  location: "",
  difficulty: "Easy",
  duration: "",
  available_slots: "",
  staff_id: "",
  status: "Open",
  trek_date: "",
});

const validateForm = () => {
  const errors = {};

  if (!form.value.trek_name.trim()) {
    errors.trek_name = "Trek name is required.";
  }

  if (!form.value.location.trim()) {
    errors.location = "Location is required.";
  }

  if (!form.value.duration || Number(form.value.duration) < 1) {
    errors.duration = "Duration must be at least 1 day.";
  }

  if (!form.value.trek_date) {
    errors.trek_date = "Trek date is required.";
  }

  if (form.value.available_slots === "" || Number(form.value.available_slots) < 0) {
    errors.available_slots = "Slots must be 0 or more.";
  }

  if (!form.value.staff_id) {
    errors.staff_id = "Please assign a staff member.";
  }

  formErrors.value = errors;
  return Object.keys(errors).length === 0;
};

const openModal = () => {
  resetForm();
  isEditing.value = false;
  editingId.value = null;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  resetForm();
};


const resetForm = () => {
  form.value = {
    trek_name: "",
    location: "",
    difficulty: "Easy",
    duration: "",
    available_slots: "",
    staff_id: "",
    status: "Open",
    trek_date: "",
  };
  formErrors.value = {};
};


const filteredTreks = computed(() => {
  const query = search.value.toLowerCase().trim();

  return treks.value.filter((trek) =>
    trek.id.toString().includes(query) ||
    trek.trek_name.toLowerCase().includes(query)
  );
});

const loadTreks = async () => {
  try {
    const response = await api.get("/admin/treks");
    treks.value = response.data;
  } catch (error) {
    console.error(error.response?.data || error);
  }
};

const loadStaff = async () => {
  try {
    const response = await api.get("/admin/staff");
    staffList.value = response.data;
  } catch (error) {
    console.error(error.response?.data || error);
  }
};

const createTrek = async () => {
  if (!validateForm()) return;

  try {
    await api.post("/admin/treks", form.value);

    closeModal();
    loadTreks();

  } catch (error) {
    console.error(error.response?.data || error);
  }
};

const editTrek = (trek) => {
  isEditing.value = true;
  editingId.value = trek.id;

form.value = {
  trek_name: trek.trek_name,
  location: trek.location,
  difficulty: trek.difficulty,
  duration: trek.duration,
  available_slots: trek.available_slots,
  staff_id: staffList.value.find(
    (staff) => staff.name === trek.staff
  )?.id,
  status: trek.status,
  trek_date: trek.trek_date || "",
};

  showModal.value = true;
};

const updateTrek = async () => {
  if (!validateForm()) return;

  try {
    await api.put(`/admin/treks/${editingId.value}`, form.value);

    closeModal();
    loadTreks();

  } catch (error) {
    console.error(error.response?.data || error);
  }
};

const openDeleteModal = (trek) => {
  selectedTrek.value = trek;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  selectedTrek.value = null;
  showDeleteModal.value = false;
};

const deleteTrek = async () => {
  try {
    await api.delete(`/admin/treks/${selectedTrek.value.id}`);

    closeDeleteModal();
    loadTreks();

  } catch (error) {
    console.error(error.response?.data || error);
  }
};

onMounted(() => {
  loadTreks();
  loadStaff();
});
</script>