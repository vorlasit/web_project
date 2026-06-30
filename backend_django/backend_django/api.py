from typing import Optional

from ninja import NinjaAPI, Schema ,Router 
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from ninja.errors import HttpError
from ninja.security import HttpBearer 

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            token = Token.objects.get(key=token)
            return token.user
        except Token.DoesNotExist:
            return None

auth = AuthBearer()

api = NinjaAPI()

router = Router(auth=auth)
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

@router.get("/profile" , auth=auth)
def get_profile(request):
    user = request.auth

    return {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }


class UserUpdateSchema(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None



@router.put("/profile_update", auth=auth)
def update_profile(request, payload: UserUpdateSchema):
    user = request.auth

    if payload.first_name is not None:
        user.first_name = payload.first_name

    if payload.last_name is not None:
        user.last_name = payload.last_name

    if payload.email is not None:
        user.email = payload.email

    user.save()

    return {
        "message": "Profile updated successfully",
        "user": {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
    }