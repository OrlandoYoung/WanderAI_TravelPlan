from django.db import models
from auth_app.models import User
from trip.models import Trip

class UserSavedTrip(models.Model):
    """用户保存的行程"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'trip')  # 确保用户不会重复保存同一行程
        
    def __str__(self):
        return f"{self.user.name}保存的{self.trip.destination}行程"