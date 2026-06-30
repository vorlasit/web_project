<template>
  <div class="container-fluid bg-dark min-vh-100 d-flex align-items-center justify-content-center p-3">

    <div class="card shadow-lg border-0 rounded-4" style="max-width: 400px; width: 100%; background: #ffffff;">
      <div class="card-body p-4 p-sm-5">

        <div class="text-center mb-4">
          <div class="d-inline-flex align-items-center justify-content-center bg-primary text-white rounded-3 mb-3"
            style="width: 50px; height: 50px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"
              stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h3 class="fw-bold text-dark mb-1">Welcome Back</h3>
          <p class="text-muted small">Please sign in to access your dashboard</p>
        </div>

        <form @submit.prevent="handleLogin">

          <div class="form-floating mb-3">
            <input id="username" type="text" class="form-control rounded-3 fs-6" v-model="username"
              placeholder="Username" required />
            <label for="username" class="text-secondary">Username</label>
          </div>

          <div class="form-floating mb-4">
            <input id="password" type="password" class="form-control rounded-3 fs-6" v-model="password"
              placeholder="Password" required />
            <label for="password" class="text-secondary">Password</label>
          </div>

          <div v-if="errorMessage" class="alert alert-danger d-flex align-items-center rounded-3 p-2 mb-3 small"
            role="alert">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24"
              stroke="currentColor" stroke-width="2" class="me-2 flex-shrink-0">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div>{{ errorMessage }}</div>
          </div>

          <button type="submit"
            class="btn btn-primary btn-lg w-100 rounded-3 fw-semibold fs-6 shadow-sm d-flex align-items-center justify-content-center">
            <span>Sign In</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24"
              stroke="currentColor" stroke-width="2" class="ms-2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>

        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Swal from 'sweetalert2';

const router = useRouter();
const username = ref('');
const password = ref('');
const errorMessage = ref('');

const handleLogin = async () => {
  try {
    errorMessage.value = '';

    const response = await axios.post('http://192.168.150.129:8000/api/login', {
      username: username.value,
      password: password.value
    });

    const token = response.data.token;
    localStorage.setItem('user-token', token);
    localStorage.setItem('username', response.data.username);

    await Swal.fire({
      icon: 'success',
      title: 'Login Successful!',
      text: 'ยินดีต้อนรับเข้าสู่ระบบ',
      confirmButtonColor: '#0d6efd',
      timer: 1500,
      timerProgressBar: true
    });

    router.push('/app/dashboard');

  } catch (error) {
    if (error.response && error.response.status === 401) {
      errorMessage.value = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง';

      Swal.fire({
        icon: 'error',
        title: 'Login Failed',
        text: 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง',
        confirmButtonColor: '#dc3545'
      });
    } else {
      errorMessage.value = 'ไม่สามารถเชื่อมต่อกับ Server หลังบ้านได้';

      Swal.fire({
        icon: 'warning',
        title: 'Connection Error',
        text: 'ไม่สามารถเชื่อมต่อกับ Server หลังบ้านได้ กรุณาเช็คการรัน Service ของ Django',
        confirmButtonColor: '#ffc107'
      });
    }
  }
};
</script>

<style scoped>
/* ⚙️ ตกแต่งสีขอบและลูกเล่นกล่องกรอกให้เข้าชุดกัน */
.form-floating>.form-control:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 0.25rem rgba(59, 130, 246, 0.25);
}

/* เพิ่มแอนิเมชันให้ตัวหนังสือตอนขยับดูนุ่มนวลขึ้น */
.form-floating>label {
  transition: transform 0.15s ease-in-out, opacity 0.15s ease-in-out;
}
</style>