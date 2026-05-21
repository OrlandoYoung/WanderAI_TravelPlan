from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/trip/', include('trip.urls')),       # 行程相关接口
    path('api/auth/', include('auth_app.urls')),   # 认证相关接口
    path('api/user/', include('user.urls')),       # 用户相关接口
    
    
]