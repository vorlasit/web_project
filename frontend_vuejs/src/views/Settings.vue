<template>
  <div class="container py-5">
    <div class="card shadow border-0 rounded-4">
      <div class="card-header bg-primary text-white">
        <h4 class="mb-0">Settings</h4>
      </div>

      <div class="card-body">
        <form @submit.prevent="saveSettings">
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input
              v-model="username"
              type="text"
              class="form-control"
              placeholder="Enter username"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input
              v-model="email"
              type="email"
              class="form-control"
              placeholder="Enter email"
            />
          </div>

          <div class="form-check form-switch mb-4">
            <input
              class="form-check-input"
              type="checkbox"
              id="darkMode"
              v-model="darkMode"
            />
            <label class="form-check-label" for="darkMode">
              Dark Mode
            </label>
          </div>

          <button type="submit" class="btn btn-primary">
            Save Changes
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Swal from "sweetalert2";

const username = ref("");
const email = ref("");
const darkMode = ref(false);

onMounted(() => {
  username.value = localStorage.getItem("username") || "";
  email.value = localStorage.getItem("email") || "";
  darkMode.value = localStorage.getItem("darkMode") === "true";
});

const saveSettings = async () => {
  localStorage.setItem("username", username.value);
  localStorage.setItem("email", email.value);
  localStorage.setItem("darkMode", darkMode.value);

  await Swal.fire({
    icon: "success",
    title: "Saved",
    text: "Your settings have been updated.",
    timer: 1500,
    showConfirmButton: false,
  });
};
</script>

<style scoped>
.card {
  max-width: 700px;
  margin: auto;
}
</style>