from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from auth_app.models import User
from trip.models import Trip
from .models import UserSavedTrip
from rest_framework.permissions import AllowAny

class UserSavedTripsView(APIView):
    """获取指定用户保存的行程列表"""
    authentication_classes = []
    permission_classes     = [AllowAny]
    
    def get(self, request, user_id):
        # 1. 根据 URL 参数获取用户
        user = get_object_or_404(User, user_id=user_id)
        
        # 2. 查询该用户的所有保存行程
        saved_trips = UserSavedTrip.objects.filter(user=user).select_related('trip')
        
        # 3. 序列化返回
        trip_list = []
        for st in saved_trips:
            t = st.trip
            trip_list.append({
                "tripId":     t.trip_id,
                "origin":     t.origin,
                "destination":t.destination,
                "startDate":  t.start_date.isoformat(),
                "endDate":    t.end_date.isoformat(),
                "status":     t.status,
                "savedAt":    st.saved_at.isoformat(),
            })
        
        return Response({
            "success":    True,
            "savedTrips": trip_list
        })

class SaveTripView(APIView):
    """保存行程"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        data = request.data
        
        # 验证必填字段
        if 'tripId' not in data:
            return Response(
                {"success": False, "error": {"message": "缺少行程ID"}},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 查找行程
        try:
            trip = Trip.objects.get(trip_id=data['tripId'])
        except Trip.DoesNotExist:
            return Response(
                {"success": False, "error": {"message": "行程不存在"}},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 检查是否已保存
        if UserSavedTrip.objects.filter(user=user, trip=trip).exists():
            return Response(
                {"success": False, "error": {"message": "行程已保存"}},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 保存行程
        UserSavedTrip.objects.create(user=user, trip=trip)
        
        # 更新用户保存的行程计数
        user.saved_trips_count = UserSavedTrip.objects.filter(user=user).count()
        user.save()
        
        return Response({
            "success": True,
            "message": "行程已保存"
        })

class UnsaveTripView(APIView):
    """取消保存行程"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        data = request.data
        
        # 验证必填字段
        if 'tripId' not in data:
            return Response(
                {"success": False, "error": {"message": "缺少行程ID"}},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 查找并删除保存的行程
        try:
            saved_trip = UserSavedTrip.objects.get(user=user, trip__trip_id=data['tripId'])
            saved_trip.delete()
            
            # 更新用户保存的行程计数
            user.saved_trips_count = UserSavedTrip.objects.filter(user=user).count()
            user.save()
            
            return Response({
                "success": True,
                "message": "行程已取消保存"
            })
        except UserSavedTrip.DoesNotExist:
            return Response(
                {"success": False, "error": {"message": "未找到保存的行程"}},
                status=status.HTTP_404_NOT_FOUND
            )

class UserTripHistoryView(APIView):
    """获取用户的行程历史（创建的行程）"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        trips = Trip.objects.filter(user=user).order_by('-created_at')
        
        trip_list = []
        for trip in trips:
            trip_list.append({
                "tripId": trip.trip_id,
                "origin": trip.origin,
                "destination": trip.destination,
                "startDate": trip.start_date.isoformat(),
                "endDate": trip.end_date.isoformat(),
                "interests": trip.interests,
                "numPeople": trip.num_people,
                "status": trip.status,
                "createdAt": trip.created_at.isoformat()
            })
        
        return Response({
            "success": True,
            "trips": trip_list
        })