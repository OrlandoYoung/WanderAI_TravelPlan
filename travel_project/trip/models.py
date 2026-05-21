from django.db import models
from django.utils import timezone

class Trip(models.Model):
    """旅行计划主模型"""
    trip_id = models.CharField(max_length=36, primary_key=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    interests = models.TextField(blank=True, null=True)
    num_people = models.IntegerField()
    user_id = models.IntegerField(blank=True, null=True)
    
    # 行程状态
    GENERATING = 'generating'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REVISING = 'revising'
    
    STATUS_CHOICES = [
        (GENERATING, '生成中'),
        (COMPLETED, '已完成'),
        (FAILED, '失败'),
        (REVISING, '修订中'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=GENERATING,
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.trip_id}: {self.origin} to {self.destination}"

class TripSummary(models.Model):
    """旅行总结"""
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, primary_key=True)
    markdown_content = models.TextField()
    
class TripWeather(models.Model):
    """天气信息"""
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, primary_key=True)
    markdown_content = models.TextField()
    
class TripTransport(models.Model):
    """交通安排"""
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, primary_key=True)
    markdown_content = models.TextField()
    
class TripHotel(models.Model):
    """住宿信息"""
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, primary_key=True)
    markdown_content = models.TextField()
    
class TripFood(models.Model):
    """美食推荐"""
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, primary_key=True)
    markdown_content = models.TextField()
    
class TripItinerary(models.Model):
    """每日行程"""
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, primary_key=True)
    markdown_content = models.TextField()
    
class TripBudget(models.Model):
    """预算明细"""
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, primary_key=True)
    markdown_content = models.TextField()