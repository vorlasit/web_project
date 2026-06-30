<template>
  <div class="container py-5">
    <div class="card p-5">
      <h2>Welcome back {{ currentUsername }}</h2>

      <!-- Dashboard Content -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const currentUsername = ref("");

onMounted(() => {
  currentUsername.value = localStorage.getItem("username") || "User";
});
</script>