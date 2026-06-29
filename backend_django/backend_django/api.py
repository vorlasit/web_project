from ninja import NinjaAPI, Schema
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from ninja.errors import HttpError

api = NinjaAPI()

# กำหนดโครงสร้างข้อมูลที่รับมาจาก Vue.js
class LoginSchema(Schema):
    username: str
    password: str

# กำหนดโครงสร้างข้อมูลที่จะตอบกลับไปหา Vue.js
class TokenSchema(Schema):
    token: str
    username: str

@api.post("/login", response=TokenSchema)
def login(request, data: LoginSchema):
    # ตรวจสอบ Username และ Password กับระบบ Django Auth
    user = authenticate(username=data.username, password=data.password) 
    if user is not None:
        # ถ้าถูกต้อง สร้างหรือดึง Token ที่เคยมีอยู่ส่งกลับไป
        token, _ = Token.objects.get_or_create(user=user)
        return {"token": token.key, "username": user.username}
    else:
        # ถ้าผิดพลาด พ่น Error 401 กลับไปบอกหน้าบ้าน
        raise HttpError(401, "Username or Password incorrect")