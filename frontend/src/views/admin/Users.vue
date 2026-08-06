<template>

  <AppLayout title="Users">

    <div class="d-flex justify-content-between align-items-center mb-4">

      <h3 class="fw-bold mb-0">
        Manage all Users
      </h3>

    </div>

    <SearchBar
      v-model="search"
      class="mb-4"
      placeholder="Search by User ID, Name or Username..."
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

          <tbody v-if="filteredUsers.length">

            <tr
              v-for="user in filteredUsers"
              :key="user.id"
            >

              <td>{{ user.id }}</td>

              <td>{{ user.name }}</td>

              <td>{{ user.username }}</td>

              <td>{{ user.email }}</td>

              <td>

                <span
                  class="badge"
                  :class="user.is_active ? 'bg-success' : 'bg-danger'"
                >
                  {{ user.is_active ? "Active" : "Inactive" }}
                </span>

              </td>

              <td class="text-center">

                <button
                  class="btn btn-sm"
                  :class="user.is_active ? 'btn-outline-danger' : 'btn-outline-success'"
                  @click="openStatusModal(user)"
                >

                  <i
                    class="bi"
                    :class="user.is_active ? 'bi-person-x' : 'bi-person-check'"
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
                No users found.
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

    <!-- Activate / Deactivate User -->

    <div
      v-if="showStatusModal"
      class="modal fade show"
      style="display:block;background:rgba(0,0,0,.5);"
    >

      <div class="modal-dialog">

        <div class="modal-content">

          <div class="modal-header">

            <h5 class="modal-title">
              {{ selectedUser?.is_active ? "Deactivate User" : "Activate User" }}
            </h5>

            <button
              class="btn-close"
              @click="closeStatusModal"
            ></button>

          </div>

          <div class="modal-body">

            <p>

              Are you sure you want to

              <strong>
                {{ selectedUser?.is_active ? "deactivate" : "activate" }}
              </strong>

              <strong>
                {{ selectedUser?.name }}
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
              :class="selectedUser?.is_active ? 'btn-danger' : 'btn-success'"
              @click="toggleStatus"
            >
              {{ selectedUser?.is_active ? "Deactivate" : "Activate" }}
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

const users = ref([]);

const search = ref("");

const showStatusModal = ref(false);

const selectedUser = ref(null);

const filteredUsers = computed(() => {
  const query = search.value.toLowerCase().trim();

  return users.value.filter((user) =>
    user.id.toString().includes(query) ||
    user.name.toLowerCase().includes(query) ||
    user.username.toLowerCase().includes(query)
  );
});

const loadUsers = async () => {
  try {
    const response = await api.get("/admin/users");
    users.value = response.data;
  } catch (error) {
    console.error(error.response?.data || error);
  }
};

const openStatusModal = (user) => {
  selectedUser.value = user;
  showStatusModal.value = true;
};

const closeStatusModal = () => {
  selectedUser.value = null;
  showStatusModal.value = false;
};

const toggleStatus = async () => {
  try {
    await api.put(`/admin/users/${selectedUser.value.id}/status`);

    closeStatusModal();
    loadUsers();

  } catch (error) {
    console.error(error.response?.data || error);
  }
};

onMounted(() => {
  loadUsers();
});
</script>