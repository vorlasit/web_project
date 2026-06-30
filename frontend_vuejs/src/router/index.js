import { createRouter, createWebHistory } from 'vue-router';

import MainLayout from "@/layouts/MainLayout.vue";
import Dashboard from "@/views/Dashboard.vue";
import Profile from "@/views/Profile.vue";
import Settings from "@/views/Settings.vue";
import Login from "@/views/Login.vue";

const routes = [
  {
    path: '/',
    name: 'login',
    component: Login
  },
  {
    path: "/app",
    component: MainLayout,
    children: [
      {
        path: "dashboard",
        component: Dashboard,
      },
      {
        path: "profile",
        component: Profile,
      },
      {
        path: "settings",
        component: Settings,
      },
    ],

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