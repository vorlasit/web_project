import { createApp } from 'vue'
import './style.css'
import App from './App.vue' 
// createApp(App).mount('#app')
import 'bootstrap/dist/css/bootstrap.min.css'
import router from './router' // 👈 1. Import router ที่เราสร้างไว้เข้ามา 
const app = createApp(App) 
app.use(router) // 👈 2. เปิดใช้งาน router ในโปรเจกต์ (นี่คือจุดที่ใช้คำสั่งนี้ครับ)

app.mount('#app')