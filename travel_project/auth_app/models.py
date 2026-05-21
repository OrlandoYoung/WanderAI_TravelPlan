from django.db import models
import uuid

# 定义独立的函数生成用户ID（替代lambda）
def generate_user_id():
    """生成唯一用户ID，格式为'u' + 8位UUID哈希"""
    return f"u{uuid.uuid4().hex[:8]}"

class User(models.Model):
    """用户模型"""
    user_id = models.CharField(
        primary_key=True, 
        max_length=50, 
        default=generate_user_id  # 使用普通函数作为默认值
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    saved_trips_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
