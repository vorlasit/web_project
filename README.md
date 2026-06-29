# web_project
# 1. ติดตั้งเครื่องมือช่วย Compile (คำสั่ง make จะมาพร้อมตัวนี้ครับ)

    sudo apt update
    sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev -y
    sudo apt install postgresql postgresql-contrib -y
# 3. เปิดใช้งาน venv แล้วติดตั้ง Django Ninja และ Django CORS

    python3.12 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip

# create file requirements.txt

    # ----------------------------------------------------
    # Core Framework & Async Server
    # ----------------------------------------------------
    Django 
    django-ninja==1.1.0        # พระเอกใหม่แทน DRF (มาพร้อม Pydantic ในตัว)
    django-cors-headers==4.3.1
    gunicorn==22.0.0
    uvicorn[standard]==0.29.0  # แนะนำให้ใช้ Uvicorn เพื่อดึงพลัง Async ของ Django Ninja ได้เต็มที่
    psycopg2-binary
    
    # ----------------------------------------------------
    # Database & Storage
    # ----------------------------------------------------
    psycopg2-binary==2.9.9     # หรือใช้อะแดปเตอร์ async อย่าง asyncpg หากเน้นเขียนโค้ดแบบ Async
    django-storages==1.14.2
    boto3==1.34.84
    
    # ----------------------------------------------------
    # Authentication & Security
    # ----------------------------------------------------
    PyJWT==2.8.0               # ใช้สำหรับเขียนระบบจัดการ JWT Token ร่วมกับ Auth ของ Django Ninja
    django-allauth==0.61.1     
    django-axes==6.3.0    
    uvloop
    nginx 
    
    # ----------------------------------------------------
    # Background Tasks & Caching
    # ----------------------------------------------------
    celery==5.3.6              
    redis==5.0.3               
    django-redis==5.4.0        
    
    # ----------------------------------------------------
    # Monitoring & Utilities
    # ----------------------------------------------------
    sentry-sdk==1.45.0         
    python-dotenv==1.0.1       
    pillow==10.3.0
# start project 

    django-admin startproject backend_django
    
# ราจะติดตั้ง Node.js เพื่อเอาไว้ใช้มัดรวมโค้ด (Build) ให้กลายเป็นไฟล์ Static ครับ:

    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install -y nodejs

# 2. สร้างโปรเจกต์ Vue 3 ด้วย Vite

    npm create vite@latest frontend_vuejs -- --template vue
    cd frontend

# 3. ติดตั้ง Dependencies และ สั่งรัน Build (เพื่อสร้างโฟลเดอร์ dist/)

    npm install
    npm run dev -- --host

# สร้างไฟล์ Service เพื่อบังคับให้ Django รันตัวเองอยู่เบื้องหลังตลาดเวลา ไม่ดับแม้ปิด SSH:

    sudo nano /etc/systemd/system/django.service
  past
  
    [Unit]
    Description=Django Backend Service
    After=network.target
    
    [Service]
    User=ubuntu
    WorkingDirectory=/var/www/my-project/backend
    # รันผ่าน venv ดึง runserver ออกมาเปิดพอร์ต 8000 ให้ภายนอกเข้าได้ตรงๆ
    ExecStart=/var/www/my-project/backend/venv/bin/python manage.py runserver 0.0.0.0:8000
    Restart=always
    
    [Install]
    WantedBy=multi-user.target

# สร้างไฟล์ Service แยกอีกตัวสำหรับรัน Vite Development Server:

    sudo nano /etc/systemd/system/vue.service
  past
  
    [Unit]
    Description=Vue Frontend Service
    After=network.target
    
    [Service]
    User=ubuntu
    WorkingDirectory=/var/www/my-project/frontend
    # สั่งรัน Vite โดยบังคับส่งพารามิเตอร์ --host เพื่อเปิดพอร์ต 5173 ให้มองเห็นจากภายนอก
    ExecStart=/usr/bin/npm run dev -- --host
    Restart=always
    # กำหนดค่า Environment เพื่อให้ทำงานได้เสถียร
    Environment=NODE_ENV=development
    
    [Install]
    WantedBy=multi-user.target

# รันชุดคำสั่งนี้เพื่อเปิดระบบจดจำสคริปต์ใหม่ และบังคับเปิดตัวรันทั้งคู่ขึ้นมาทันทีครับ:
  # 1. รีโหลดระบบสคริปต์ Systemd
  
    sudo systemctl daemon-reload
  
  # 2. เปิดใช้งานและสั่งให้เปิดโปรแกรมอัติโนมัติตอนเปิดเครื่อง
  
    sudo systemctl enable django
    sudo systemctl enable vue
  
  # 3. สั่ง Start เริ่มทำงานทันที
    
    sudo systemctl start django
    sudo systemctl start vue
  # คุณสามารถเช็คดูว่า Service แต่ละตัวทำงานถูกต้องและไม่มี Error ไหมด้วยคำสั่งนี้ครับ:
  
    sudo systemctl status django   # เช็คสถานะหลังบ้าน
    sudo systemctl status vue      # เช็คสถานะหน้าบ้าน
# 2. สลับสิทธิ์เข้าไปในระบบของ postgres เพื่อเปิดหน้าจอบริหารข้อมูล
    
    sudo -i -u postgres psql
  เมื่อคุณรันคำสั่งที่ 2 หน้าจอจะเปลี่ยนสิทธิ์เป็นสัญลักษณ์ postgres=# ให้พิมพ์คำสั่ง SQL ด้านล่างนี้ทีละบรรทัดเพื่อสร้าง Database และสิทธิ์การเข้าถึงครับ:
    
    -- สร้างฐานข้อมูลชื่อ my_django_db
    CREATE DATABASE my_django_db;
    
    -- สร้าง User ชื่อ my_django_user พร้อมรหัสผ่านที่คุณต้องการ (เปลี่ยนตรง 'password_here' ได้)
    CREATE USER my_django_user WITH PASSWORD 'password_here';
    
    -- ตั้งค่ามาตรฐานของ Encoding และ Timezone ให้ทำงานร่วมกับ Python ได้ดี
    ALTER ROLE my_django_user SET client_encoding TO 'utf8';
    ALTER ROLE my_django_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE my_django_user SET timezone TO 'UTC';
    
    -- มอบสิทธิ์จัดการทั้งหมดของ Database นี้ให้กับ User ที่พึ่งสร้าง
    GRANT ALL PRIVILEGES ON DATABASE my_django_db TO my_django_user;
    
    -- พิมพ์คำสั่งเพื่อออกจากระะบบฐานข้อมูลกลับมาหน้าจอ Ubuntu ปกติ
    \q
    exit

# จากนั้นเปิดไฟล์ core/settings.py ขึ้นมาแก้ไข (เช่นใช้คำสั่ง nano core/settings.py) มองหาคำว่า DATABASES เดิมที่เป็นของ SQLite แล้วเปลี่ยนเป็นค่าของ PostgreSQL ที่เราพึ่งตั้งค่าเมื่อครู่ดังนี้ครับ:
  # แก้ไขใน core/settings.py
  
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'my_django_db',
            'USER': 'my_django_user',
            'PASSWORD': 'password_here',  # ใส่รหัสผ่านที่คุณตั้งไว้ในขั้นตอนที่ 1
            'HOST': '127.0.0.1',           # รันอยู่ในเครื่อง Server เดียวกัน
            'PORT': '5432',                # พอร์ตมาตรฐานของ PostgreSQL
        }
    }
migare for backend

        python manage.py migrate
create super user
        
        python manage.py createsuperuser
# ติดตั้ง Vue Router (ถ้ายังไม่มี)

        npm install vue-router@4
# สร้างไฟล์สำหรับกำหนดเส้นทางเว็บขึ้นมา เช่น src/router/index.js เพื่อบอกระบบว่า Path ไหนคู่กับหน้าจอไหน:

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
            // 🔒 ป้องกันไม่ให้แอบเข้าหน้านี้ถ้ายังไม่ได้ล็อกอิน
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
# อัปเดตไฟล์ App.vue

        <template>
          <div id="app">
            <router-view />
          </div>
        </template>
        
        <script setup>
        // ใน App.vue ยุคใหม่ ไม่ต้อง Import Component มาวางตรงๆ แล้ว ปล่อยให้ Router จัดการสลับหน้าให้ครับ
        </script>
# // 👈 1. Import ตัวช่วยเปลี่ยนหน้าเข้ามา

        import { useRouter } from 'vue-router'; 
        const router = useRouter(); // 👈 2. ประกาศใช้งาน Router Instance
        
# เพื่อให้คลาสของ Bootstrap เช่น d-flex, card, btn-primary แสดงผลได้อย่างสมบูรณ์ อย่าลืมตรวจสอบว่าคุณได้เรียกใช้ Bootstrap เข้ามาในโปรเจกต์ Vue แล้วหรือยัง:

        npm install bootstrap
# จากนั้นเปิดไฟล์ src/main.js แล้วทำการเพิ่มบรรทัด Import ตัว CSS ของ Bootstrap ไว้ด้านบนสุด เพื่อให้ทุกหน้าเรียกใช้งานได้ร่วมกันครับ:

        import { createApp } from 'vue'
        import App from './App.vue'
        import router from './router' // เพี่ม router
        
        // 🟢 เพิ่มบรรทัดนี้เข้ามาเพื่อเรียกใช้ Bootstrap CSS
        import 'bootstrap/dist/css/bootstrap.min.css' 
        
        const app = createApp(App)
        app.use(router)
        app.mount('#app')
# ติดตั้ง SweetAlert2

        npm install sweetalert2
# อัปเดตโค้ดหน้า Login ด้วย SweetAlert2

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
                    <input 
                      id="username" 
                      type="text" 
                      class="form-control rounded-3 fs-6" 
                      v-model="username"
                      placeholder="Username" 
                      required 
                    />
                    <label for="username" class="text-secondary">Username</label>
                  </div>
        
                  <div class="form-floating mb-4"> 
                    <input 
                      id="password" 
                      type="password" 
                      class="form-control rounded-3 fs-6" 
                      v-model="password"
                      placeholder="Password" 
                      required 
                    />
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
        
            router.push('/dashboard');
        
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
        .form-floating > .form-control:focus {
          border-color: #3b82f6;
          box-shadow: 0 0 0 0.25rem rgba(59, 130, 246, 0.25);
        }
        
        /* เพิ่มแอนิเมชันให้ตัวหนังสือตอนขยับดูนุ่มนวลขึ้น */
        .form-floating > label {
          transition: transform 0.15s ease-in-out, opacity 0.15s ease-in-out;
        }
        </style>
    
# โค้ดเวอร์ชันแก้ไขที่สมบูรณ์และสวยงาม
คุณสามารถคัดลอกโค้ดชุดนี้ไปทับในไฟล์ Dashboard

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


        
