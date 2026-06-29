<template>
  <div class="container-fluid min-vh-100 bg-light d-flex flex-column p-0">
    
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 shadow-sm">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold d-flex align-items-center" href="#">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" class="me-2 text-primary">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11 3.055A9.003 9.003 0 1020.945 13H11V3.055z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
          </svg>
          DevNext Dashboard
        </a>
        
        <div class="d-flex align-items-center text-white">
          <span class="me-3 small d-none d-sm-inline text-muted">Logged in as:</span>
          <span class="badge bg-secondary px-3 py-2 rounded-pill fw-semibold">{{ currentUsername }}</span>
        </div>
      </div>
    </nav>

    <div class="container flex-grow-1 d-flex align-items-center justify-content-center py-5">
      <div class="card shadow border-0 rounded-4 p-4 p-md-5 bg-white w-100" style="max-width: 700px;">
        
        <div class="text-center mb-4">
          <h2 class="fw-bold text-dark">Welcome back, {{ currentUsername }}! ✨</h2>
          <p class="text-muted">นี่คือพื้นที่ข้อมูลภายในระบบของคุณ จัดการและตรวจสอบสถิติได้ที่นี่</p>
        </div>

        <hr class="text-muted my-4" />

        <div class="row g-3 mb-4">
          <div class="col-6 col-md-4">
            <div class="p-3 bg-light rounded-3 text-center border">
              <span class="text-muted small d-block mb-1">Status</span>
              <span class="badge bg-success">Active</span>
            </div>
          </div>
          <div class="col-6 col-md-4">
            <div class="p-3 bg-light rounded-3 text-center border">
              <span class="text-muted small d-block mb-1">Role</span>
              <span class="fw-bold text-secondary">Administrator</span>
            </div>
          </div>
          <div class="col-12 col-md-4">
            <div class="p-3 bg-light rounded-3 text-center border">
              <span class="text-muted small d-block mb-1">Session Token</span>
              <span class="text-truncate d-block small text-primary fw-mono">Valid & Secured</span>
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-center mt-2">
          <button @click="handleLogout" class="btn btn-outline-danger px-4 py-2 rounded-3 fw-semibold d-flex align-items-center shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" class="me-2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span>Sign Out</span>
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Swal from 'sweetalert2'; // 👈 อย่าลืมสั่ง Import เข้ามาใช้ในหน้านี้ด้วยครับ

const router = useRouter();
const currentUsername = ref('');

onMounted(() => {
  // ดึงชื่อคนที่ Login ที่เรา Save ไว้ใน LocalStorage ออกมาโชว์
  currentUsername.value = localStorage.getItem('username') || 'User';
});

// ✅ แก้ไขซ้อนฟังก์ชัน และคุม Flow ให้กระโดดหน้าหลังจากกดผ่าน SweetAlert เท่านั้น
const handleLogout = () => {
  Swal.fire({
    title: 'Are you sure?',
    text: "คุณต้องการออกจากระบบใช่หรือไม่?",
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#dc3545', // สีแดงตามธีมปุ่มออก
    cancelButtonColor: '#6c757d',
    confirmButtonText: 'ใช่, ออกจากระบบ',
    cancelButtonText: 'ยกเลิก',
    reverseButtons: true // สลับเอาปุ่มยืนยันไว้ฝั่งขวาตามหลักสากล
  }).then((result) => {
    if (result.isConfirmed) {
      // 🧼 ล้างข้อมูลสิทธิ์ทั้งหมดออกจาก Browser
      localStorage.removeItem('user-token');
      localStorage.removeItem('username');

      // 🚪 เด้งกลับไปหน้าแรกหลังจากผู้ใช้กดตกลง
      router.push('/');
    }
  });
};
</script>

<style scoped>
/* เพิ่มฟอนต์สไตล์โมเดิร์นเล็กน้อย */
.fw-mono {
  font-family: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}
</style>