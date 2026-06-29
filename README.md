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
    
