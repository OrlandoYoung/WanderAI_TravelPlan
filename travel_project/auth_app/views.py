from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
import bcrypt
import random
from django.core.mail import send_mail
from django.conf import settings
import time

email_code_cache = {}

class SendEmailCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if isinstance(email, dict):
            email = email.get('email')
        if not email:
            return Response({"success": False, "error": {"message": "邮箱不能为空"}}, status=400)
        if User.objects.filter(email=email).exists():
            return Response({"success": False, "error": {"message": "邮箱已被注册"}}, status=400)
        code = str(random.randint(100000, 999999))
        # 发送邮件
        send_mail(
            subject='WanderAI 注册验证码',
            message=f'您的验证码是：{code},5分钟内有效。',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        email_code_cache[email] = (code, time.time())
        return Response({"success": True, "message": "验证码已发送"})
    
class RegisterView(APIView):
    """用户注册视图"""
    def post(self, request):
        data = request.data
        # 验证邮箱验证码
        email = data.get('email')
        code = data.get('code')
        real_code_tuple = email_code_cache.get(email)
        if not real_code_tuple:
            return Response({"success": False, "error": {"message": "验证码错误或已过期"}}, status=400)
        real_code, send_time = real_code_tuple
        if code != real_code or time.time() - send_time > 300:
            return Response({"success": False, "error": {"message": "验证码错误或已过期"}}, status=400)
        # 删除验证码，防止重复使用
        del email_code_cache[email]
        # 验证必填字段
        required_fields = ['name', 'email', 'password']
        if not all(field in data for field in required_fields):
            return Response(
                {"success": False, "error": {"message": "缺少必要参数"}},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查邮箱是否已注册
        if User.objects.filter(email=data['email']).exists():
            return Response(
                {"success": False, "error": {"message": "邮箱已被注册"}},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 加密密码
        password_hash = bcrypt.hashpw(
            data['password'].encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # 创建用户
        user = User.objects.create(
            name=data['name'],
            email=data['email'],
            password_hash=password_hash
        )
        
        # 生成JWT令牌
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "success": True,
            "user": {
                "userId": user.user_id,
                "name": user.name,
                "email": user.email
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """用户登录视图"""
    def post(self, request):
        data = request.data
        
        # 验证必填字段
        required_fields = ['email', 'password']
        if not all(field in data for field in required_fields):
            return Response(
                {"success": False, "error": {"message": "缺少必要参数"}},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 查找用户
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return Response(
                {"success": False, "error": {"message": "邮箱或密码错误"}},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # 验证密码
        if not bcrypt.checkpw(
            data['password'].encode('utf-8'), 
            user.password_hash.encode('utf-8')
        ):
            return Response(
                {"success": False, "error": {"message": "邮箱或密码错误"}},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # 生成JWT令牌
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "success": True,
            "user": {
                "userId": user.user_id,
                "name": user.name,
                "email": user.email,
                "savedTripsCount": user.saved_trips_count
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        })

class LogoutView(APIView):
    """用户登出视图"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # 使刷新令牌失效
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": True, "message": "成功登出"})
        except Exception as e:
            return Response(
                {"success": False, "error": {"message": "登出失败"}},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserProfileView(APIView):
    """用户资料视图"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 返回当前认证用户的资料
        user = request.user
        return Response({
            "success": True,
            "user": {
                "userId": user.user_id,
                "name": user.name,
                "email": user.email,
                "savedTripsCount": user.saved_trips_count,
                "createdAt": user.created_at.isoformat()
            }
        })
    
    def put(self, request):
        # 更新用户资料
        user = request.user
        data = request.data
        
        # 更新可选字段
        if 'name' in data:
            user.name = data['name']
        
        user.save()
        
        return Response({
            "success": True,
            "user": {
                "userId": user.user_id,
                "name": user.name,
                "email": user.email,
                "savedTripsCount": user.saved_trips_count
            }
        })