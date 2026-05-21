from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
import uuid
import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse

from .models import (
    Trip, TripSummary, TripWeather, TripTransport,
    TripHotel, TripFood, TripItinerary, TripBudget
)
from tasks.tasks import TravelTasks
from main import TripCrew  # 行程生成核心逻辑
from crewai import Crew, Process
from agents import TravelAgents
from user.models import UserSavedTrip
from auth_app.models import User
from rest_framework.permissions import AllowAny
from uuid import uuid4

logger = logging.getLogger(__name__)


class GenerateTripView(APIView):
    """
    生成旅行计划并自动保存到用户的“已保存行程”表。
    必须提供 userId，先验证用户存在再创建 Trip 和生成计划。
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        # 1. 检查是否包含 userId，并确认用户存在
        user_id = data.get('userId')
        if not user_id:
            return Response(
                {"success": False, "error": {"message": "缺少必要参数：userId"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(
                {"success": False, "error": {"message": f"用户 {user_id} 不存在"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. 验证其他必填参数
        required_fields = ['origin', 'destination', 'startDate', 'endDate', 'numPeople']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return Response(
                {"success": False, "error": {"message": f"缺少必要参数：{', '.join(missing_fields)}"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. 解析日期格式
        try:
            start_date = datetime.strptime(data['startDate'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['endDate'], '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"success": False, "error": {"message": "日期格式错误，应为 YYYY-MM-DD"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. 创建 Trip 记录
        trip_id = f"t{uuid4().hex[:8]}"
        trip = Trip.objects.create(
            trip_id=trip_id,
            origin=data['origin'],
            destination=data['destination'],
            start_date=start_date,
            end_date=end_date,
            interests=data.get('interests', ''),
            num_people=data['numPeople'],
            status=Trip.GENERATING,
        )

        # 5. 调用 TripCrew 生成行程
        try:
            crew = TripCrew(
                origin=data['origin'],
                destination=data['destination'],
                date_range=f"{start_date}至{end_date}",
                interests=data.get('interests', ''),
                person=data['numPeople'],
                trip_id=trip_id,
                max_workers=5
            )
            crew.run()

            # 6. 更新状态 & 保存用户行程
            trip.status = Trip.COMPLETED
            trip.save()

            UserSavedTrip.objects.get_or_create(user=user, trip=trip)

            # 7. 返回成功响应
            return Response({
                "success": True,
                "tripId": trip_id,
                "message": "旅行计划已生成并已保存"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            trip.status = Trip.FAILED
            trip.save()
            return Response(
                {"success": False, "error": {"message": f"生成失败：{e}"}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DownloadTripView(APIView):
    def get(self, request, trip_id):
        print(f"[DEBUG] 请求下载 trip_id={trip_id}")  # 确保这个打印输出能在终端中看到
        
        try:
            # 获取 Trip 实例
            trip = get_object_or_404(Trip, trip_id=trip_id)
            print(f"[DEBUG] 找到 Trip: {trip}")

            # 获取 TripSummary
            summary = get_object_or_404(TripSummary, trip=trip)
            print(f"[DEBUG] 找到 TripSummary: {summary}")

            content = summary.markdown_content or "# 无内容"
            fmt = request.query_params.get('format', 'md')  # 获取format参数，默认是'md'
            print(f"[DEBUG] 请求格式: {fmt}")

            if fmt == 'md':
                response = HttpResponse(content, content_type='text/markdown')
                response['Content-Disposition'] = f'attachment; filename="{trip_id}.md"'
            elif fmt == 'txt':
                response = HttpResponse(content, content_type='text/plain')
                response['Content-Disposition'] = f'attachment; filename="{trip_id}.txt"'
            elif fmt == 'pdf':
                from reportlab.pdfgen import canvas
                from reportlab.lib.pagesizes import letter
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{trip_id}.pdf"'
                p = canvas.Canvas(response, pagesize=letter)
                p.drawString(50, 800, content[:500])
                p.showPage()
                p.save()
            else:
                return Response({"error": "不支持的格式"}, status=400)

            return response

        except Exception as e:
            print(f"[ERROR] 下载失败: {e}")
            return Response({"error": str(e)}, status=500)


class TripSummaryView(APIView):
    """获取行程总结"""
    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, trip_id=trip_id)
        try:
            summary = TripSummary.objects.get(trip=trip)
            return Response({"success": True, "markdown": summary.markdown_content})
        except TripSummary.DoesNotExist:
            return Response(
                {"success": False, "error": {"message": "行程总结不存在"}},
                status=status.HTTP_404_NOT_FOUND
            )


class TripWeatherView(APIView):
    """获取天气信息"""
    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, trip_id=trip_id)
        try:
            weather = TripWeather.objects.get(trip=trip)
            return Response({"success": True, "markdown": weather.markdown_content})
        except TripWeather.DoesNotExist:
            logger.error(f"Weather not found for trip {trip_id}")
            return Response(
                {"success": False, "error": {"message": "天气信息不存在"}},
                status=status.HTTP_404_NOT_FOUND
            )


class TripTransportView(APIView):
    """获取交通安排"""
    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, trip_id=trip_id)
        try:
            transport = TripTransport.objects.get(trip=trip)
            return Response({"success": True, "markdown": transport.markdown_content})
        except TripTransport.DoesNotExist:
            return Response(
                {"success": False, "error": {"message": "交通信息不存在"}},
                status=status.HTTP_404_NOT_FOUND
            )


class TripHotelView(APIView):
    """获取住宿信息"""
    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, trip_id=trip_id)
        try:
            hotel = TripHotel.objects.get(trip=trip)
            return Response({"success": True, "markdown": hotel.markdown_content})
        except TripHotel.DoesNotExist:
            return Response(
                {"success": False, "error": {"message": "住宿信息不存在"}},
                status=status.HTTP_404_NOT_FOUND
            )


class TripFoodView(APIView):
    """获取美食推荐"""
    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, trip_id=trip_id)
        try:
            food = TripFood.objects.get(trip=trip)
            return Response({"success": True, "markdown": food.markdown_content})
        except TripFood.DoesNotExist:
            return Response(
                {"success": False, "error": {"message": "美食信息不存在"}},
                status=status.HTTP_404_NOT_FOUND
            )


class TripItineraryView(APIView):
    """获取每日行程"""
    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, trip_id=trip_id)
        try:
            itinerary = TripItinerary.objects.get(trip=trip)
            return Response({"success": True, "markdown": itinerary.markdown_content})
        except TripItinerary.DoesNotExist:
            return Response(
                {"success": False, "error": {"message": "行程安排不存在"}},
                status=status.HTTP_404_NOT_FOUND
            )


class TripBudgetView(APIView):
    """获取预算明细"""
    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, trip_id=trip_id)
        try:
            budget = TripBudget.objects.get(trip=trip)
            return Response({"success": True, "markdown": budget.markdown_content})
        except TripBudget.DoesNotExist:
            return Response(
                {"success": False, "error": {"message": "预算信息不存在"}},
                status=status.HTTP_404_NOT_FOUND
            )


class TripStatusView(APIView):
    """获取行程状态"""
    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, trip_id=trip_id)
        return Response({
            "success": True,
            "status": trip.status,
            "updatedAt": trip.updated_at.isoformat()
        })


class RegenerateTripView(APIView):
    """重新生成行程（保留原行程ID），并覆盖 TripSummary 和 UserSavedTrip 记录。"""
    permission_classes = [AllowAny]

    def post(self, request, trip_id):
        # 1. 获取旧 Trip
        trip = get_object_or_404(Trip, trip_id=trip_id)

        # 2. 校验状态
        if trip.status == Trip.GENERATING:
            return Response(
                {"success": False, "error": {"message": "行程正在生成中，请稍后再试"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. 标记重新生成中
        trip.status = Trip.GENERATING
        trip.save(update_fields=['status'])

        # 4. 验证 userId
        user_id = request.data.get('userId')
        if not user_id:
            return Response(
                {"success": False, "error": {"message": "缺少 userId"}},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_object_or_404(User, user_id=user_id)

        try:
            with transaction.atomic():
                # 5. 执行新一轮 TripCrew 生成（内部已通过 update_or_create 更新 TripSummary）
                crew = TripCrew(
                    origin=trip.origin,
                    destination=trip.destination,
                    date_range=f"{trip.start_date}至{trip.end_date}",
                    interests=trip.interests,
                    person=trip.num_people,
                    trip_id=trip_id,
                    max_workers=5
                )
                crew.run()

                # 6. 覆盖 UserSavedTrip: 删除旧记录并重建保存时间
                UserSavedTrip.objects.filter(user=user, trip=trip).delete()
                UserSavedTrip.objects.create(user=user, trip=trip)

                # 7. 完成标记
                trip.status = Trip.COMPLETED
                trip.save(update_fields=['status'])

            return Response({"success": True, "message": "行程已重新生成并覆盖原始数据"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(f"重新生成失败: trip_id={trip_id}")
            trip.status = Trip.FAILED
            trip.save(update_fields=['status'])
            return Response(
                {"success": False, "error": {"message": f"重新生成失败：{e}"}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteTripView(APIView):
    """删除行程（级联删除所有关联数据）"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, trip_id):
        trip = get_object_or_404(Trip, trip_id=trip_id)
        if request.user.is_authenticated and trip.user_id != request.user.id:
            return Response(
                {"success": False, "error": {"message": "无权删除此行程"}},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            trip.delete()
            return Response({"success": True, "message": "行程已删除"})
        except Exception as e:
            logger.exception(f"删除失败: trip_id={trip_id}")
            return Response(
                {"success": False, "error": {"message": f"删除失败：{str(e)}"}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReviseTripPlanView(APIView):
    """根据用户反馈修订旅行计划"""
    def post(self, request, trip_id):
        # 1. 尝试标准字段
        data = request.data or {}
        feedback = data.get('user_feedback') or data.get('feedback') or data.get('userFeedback')

        # 2. 如果还没拿到，从 data 的第一个项取
        if not feedback and isinstance(data, dict) and data:
            first_key = next(iter(data))
            feedback = data[first_key]

        # 3. 如果还没，从原始 body 读取
        if not feedback and request.body:
            try:
                feedback = request.body.decode('utf-8').strip()
            except:
                pass

        if not feedback:
            return Response(
                {"success": False, "error": {"message": "缺少修订意见，请在请求体 JSON 中提供 'user_feedback' 或 'feedback'"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. 检查行程状态
        trip = get_object_or_404(Trip, trip_id=trip_id)
        if trip.status not in [Trip.COMPLETED, Trip.REVISING]:
            return Response(
                {"success": False, "error": {"message": f"当前状态 '{trip.get_status_display()}'，无法修订"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 5. 找到原始内容
        try:
            summary = TripSummary.objects.get(trip=trip)
        except TripSummary.DoesNotExist:
            return Response(
                {"success": False, "error": {"message": "未找到原始行程，无法修订"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 6. 标记修订中
        trip.status = Trip.REVISING
        trip.save()
        logger.info(f"开始修订: trip_id={trip_id}, feedback={feedback[:50]}")

        # 7. 调用 Agent 修订
        try:
            # 获取 Trip_Planner_Agent
            ta = TravelAgents()
            planner_agent = ta.Trip_Planner_Agent()

            # 生成 Revise_Plan 任务
            tasks = TravelTasks()
            revise_task = tasks.Revise_Plan(
                planner_agent,
                previous_plan=summary.markdown_content,
                user_feedback=feedback
            )

            # 执行并获取结果
            revised_out = Crew(
                agents=[planner_agent],
                tasks=[revise_task],
                process=Process.sequential,
                verbose=True
            ).kickoff({
                "previous_plan": summary.markdown_content,
                "user_feedback": feedback
            })

            revised_md = str(revised_out)

            # 保存新内容
            summary.markdown_content = revised_md
            summary.save()
            trip.status = Trip.COMPLETED
            trip.save()
            logger.info(f"修订成功: trip_id={trip_id}")

            return Response({"success": True, "message": "行程修订成功"})

        except Exception as e:
            logger.exception(f"修订失败: trip_id={trip_id}")
            trip.status = Trip.FAILED
            trip.save()
            return Response(
                {"success": False, "error": {"message": "行程修订失败，请稍后重试"}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
