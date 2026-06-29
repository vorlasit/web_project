import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue'; // ทางไปหน้า Login ของคุณ
import Dashboard from '../components/Dashboard.vue'; // หน้า Dashboard ที่จะสร้างใหม่

const routes = [
  {
    path: '/',
    name: 'login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    // # 🔒 ป้องกันไม่ให้แอบเข้าหน้านี้ถ้ายังไม่ได้ล็อกอิน
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('user-token');
      if (token) {
        next(); // มี Token ให้เข้าได้
      } else {
        next('/'); // ไม่มี Token ส่งกลับไปหน้า Login
      }
    }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;