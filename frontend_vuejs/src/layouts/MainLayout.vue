<template>
  <div class="container-fluid min-vh-100 bg-light p-0">
    <AppNavbar />

    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import AppNavbar from "@/components/AppNavbar.vue";
</script>