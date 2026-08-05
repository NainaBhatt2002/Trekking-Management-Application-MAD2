<template>
  <AdminLayout title="Staff">

    <div class="d-flex justify-content-between align-items-center mb-4">

      <h3 class="fw-bold mb-0">
        Manage all Staff
      </h3>

      <button
        class="btn btn-primary"
        @click="openModal"
      >
        <i class="bi bi-plus-lg me-2"></i>
        Add Staff
      </button>

    </div>

    <SearchBar
      v-model="search"
      class="mb-4"
      placeholder="Search by Staff ID or Name"
    />

    <div class="card border-0 shadow-sm rounded-4">

      <div class="card-body">

        <table class="table table-hover align-middle">

          <thead>

            <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Username</th>
            <th>Email</th>
            <th>Status</th>
              <th class="text-center">Actions</th>
            </tr>

          </thead>

          <tbody v-if="filteredStaff.length">

            <tr
              v-for="member in filteredStaff"
              :key="member.id"
            >

              <td>{{ member.id }}</td>
              <td>{{ member.name }}</td>
              <td>{{ member.username }}</td>
              <td>{{ member.email }}</td>

              <td>

                <span
                  class="badge"
                  :class="member.is_active ? 'bg-success' : 'bg-danger'"
                >
                  {{ member.is_active ? "Active" : "Inactive" }}
                </span>

              </td>

              <td class="text-center">

                <button
                  class="btn btn-sm btn-outline-primary me-2"
                  @click="editStaff(member)"
                >
                  <i class="bi bi-pencil"></i>
                </button>

                <button
                  class="btn btn-sm"
                  :class="member.is_active ? 'btn-outline-danger' : 'btn-outline-success'"
                  @click="openStatusModal(member)"
                >
                  <i
                    class="bi"
                    :class="member.is_active ? 'bi-person-x' : 'bi-person-check'"
                  ></i>
                </button>

              </td>

            </tr>

          </tbody>

          <tbody v-else>

            <tr>

              <td
                colspan="6"
                class="text-center text-muted py-5"
              >
                No staff found.
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

    <!-- Add / Edit Staff Pop Up -->

    <div
      v-if="showModal"
      class="modal fade show"
      style="display:block;background:rgba(0,0,0,.5);"
    >

      <div class="modal-dialog">

        <div class="modal-content">

          <div class="modal-header">

            <h5 class="modal-title">
              {{ isEditing ? "Edit Staff" : "Add Staff" }}
            </h5>

            <button
              class="btn-close"
              @click="closeModal"
            ></button>

          </div>

          <div class="modal-body">

            <div class="mb-3">

              <label class="form-label">
                Name
              </label>

              <input
                v-model="form.name"
                type="text"
                class="form-control"
              >

            </div>

            <div class="mb-3">

              <label class="form-label">
                Username
              </label>

              <input
                v-model="form.username"
                type="text"
                class="form-control"
              >

            </div>

            <div class="mb-3">

              <label class="form-label">
                Email
              </label>

              <input
                v-model="form.email"
                type="email"
                class="form-control"
              >

            </div>

            <div class="mb-3">

              <label class="form-label">
                Password
              </label>

              <input
                v-model="form.password"
                type="password"
                class="form-control"
                :placeholder="isEditing ? 'Leave blank to keep current password' : 'Enter password'"
              >

            </div>

          </div>

          <div class="modal-footer">

            <button
              class="btn btn-secondary"
              @click="closeModal"
            >
              Cancel
            </button>

            <button
              class="btn btn-primary"
              @click="isEditing ? updateStaff() : createStaff()"
            >
              {{ isEditing ? "Update Staff" : "Create Staff" }}
            </button>

          </div>

        </div>

      </div>

    </div>

        <!-- Activate / Deactivate Staff Pop up -->

    <div
      v-if="showStatusModal"
      class="modal fade show"
      style="display:block;background:rgba(0,0,0,.5);"
    >

      <div class="modal-dialog">

        <div class="modal-content">

          <div class="modal-header">

            <h5 class="modal-title">
              {{ selectedStaff?.is_active ? "Deactivate Staff" : "Activate Staff" }}
            </h5>

            <button
              type="button"
              class="btn-close"
              @click="closeStatusModal"
            ></button>

          </div>

          <div class="modal-body">

            <p class="mb-0">

              Are you sure you want to

              <strong>
                {{ selectedStaff?.is_active ? "deactivate" : "activate" }}
              </strong>

              <strong>
                {{ selectedStaff?.name }}
              </strong>?

            </p>

          </div>

          <div class="modal-footer">

            <button
              class="btn btn-secondary"
              @click="closeStatusModal"
            >
              Cancel
            </button>

            <button
              class="btn"
              :class="selectedStaff?.is_active ? 'btn-danger' : 'btn-success'"
              @click="toggleStatus"
            >
              {{ selectedStaff?.is_active ? "Deactivate" : "Activate" }}
            </button>

          </div>

        </div>

      </div>

    </div>

  </AdminLayout>

</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../../services/api";
import AdminLayout from "../../components/AdminLayout.vue";
import SearchBar from "../../components/SearchBar.vue";

const staff = ref([]);
const search = ref("");
const showModal = ref(false);
const showStatusModal = ref(false);
const isEditing = ref(false);
const editingId = ref(null);
const selectedStaff = ref(null);

const form = ref({
  name: "",
  username: "",
  email: "",
  password: "",
});

const resetForm = () => {
  form.value = {
    name: "",
    username: "",
    email: "",
    password: "",
  };
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

const openStatusModal = (member) => {
  selectedStaff.value = member;
  showStatusModal.value = true;
};

const closeStatusModal = () => {
  selectedStaff.value = null;
  showStatusModal.value = false;
};

const filteredStaff = computed(() => {
  const query = search.value.toLowerCase().trim();

  return staff.value.filter((member) =>
    member.id.toString().includes(query) ||
    member.name.toLowerCase().includes(query) ||
    member.email.toLowerCase().includes(query)
  );
});

const loadStaff = async () => {
  try {
    const response = await api.get("/admin/staff");
    staff.value = response.data;
  } catch (error) {
    console.error(error.response?.data || error);
  }
};

const createStaff = async () => {
  try {
    await api.post("/admin/staff", form.value);

    closeModal();
    loadStaff();

  } catch (error) {
    console.error(error.response?.data || error);
  }
};

const editStaff = (member) => {
  isEditing.value = true;
  editingId.value = member.id;

  form.value = {
    name: member.name,
    username: member.username,
    email: member.email,
    password: "",
  };

  showModal.value = true;
};

const updateStaff = async () => {
  try {
    await api.put(`/admin/staff/${editingId.value}`, form.value);

    closeModal();
    loadStaff();

  } catch (error) {
    console.error(error.response?.data || error);
  }
};

const toggleStatus = async () => {
  try {
    await api.put(`/admin/staff/${selectedStaff.value.id}/status`);

    closeStatusModal();
    loadStaff();

  } catch (error) {
    console.error(error.response?.data || error);
  }
};

onMounted(() => {
  loadStaff();
});
</script>