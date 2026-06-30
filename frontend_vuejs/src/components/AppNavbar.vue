<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 shadow-sm">
    <div class="container-fluid">
      <router-link class="navbar-brand fw-bold d-flex align-items-center" to="/app/dashboard">
        DevNext Dashboard
      </router-link>
      <button class="btn btn-sm btn-outline-light me-3" @click="toggleTheme">
        <i :class="isDark ? 'bi bi-moon-fill' : 'bi bi-sun-fill'"></i>
      </button>
      <div class="dropdown">
        <button class="btn btn-dark dropdown-toggle d-flex align-items-center" type="button" data-bs-toggle="dropdown"
          aria-expanded="false">
          <i class="bi bi-person-circle me-2"></i>
          {{ username }}
        </button>

        <ul class="dropdown-menu dropdown-menu-end shadow">
          <li>
            <router-link class="dropdown-item" to="/app/profile">
              <i class="bi bi-person me-2"></i>
              Profile
            </router-link>
          </li>

          <li>
            <hr class="dropdown-divider" />
          </li>

          <li>
            <button class="dropdown-item text-danger" @click="handleLogout">
              <i class="bi bi-box-arrow-right me-2"></i>
              Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Swal from "sweetalert2";

const router = useRouter();

const goToProfile = () => {
  router.push("/app/profile");
};
const goToDashboard = () => {
  router.push("/app/dashboard");
};

const username = ref("User");
const isDark = ref(false);
 const toggleTheme = () => {
  isDark.value = !isDark.value;

  if (isDark.value) {
    document.body.classList.add("dark-mode");
    localStorage.setItem("theme", "dark");
  } else {
    document.body.classList.remove("dark-mode");
    localStorage.setItem("theme", "light");
  }
};
onMounted(() => {
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme === "dark") {
    isDark.value = true;
    document.body.classList.add("dark-mode");
  }
  username.value = localStorage.getItem("username") || "User";
});

const handleLogout = async () => {
  const result = await Swal.fire({
    title: "Are you sure?",
    text: "คุณต้องการออกจากระบบใช่หรือไม่?",
    icon: "question",
    showCancelButton: true,
    confirmButtonText: "Logout",
    cancelButtonText: "Cancel",
    confirmButtonColor: "#dc3545",
  });

  if (result.isConfirmed) {
    localStorage.removeItem("username");
    localStorage.removeItem("user-token");

    router.push("/");
  }
};
</script>