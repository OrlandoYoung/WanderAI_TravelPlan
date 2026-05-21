from django.urls import path
from .views import (
    GenerateTripView, TripSummaryView, TripWeatherView, 
    TripTransportView, TripHotelView, TripFoodView, 
    TripItineraryView, TripBudgetView, TripStatusView,
    RegenerateTripView, DeleteTripView, ReviseTripPlanView,
    DownloadTripView
)

urlpatterns = [
    path('generate', GenerateTripView.as_view(), name='generate_trip'),
    path('<str:trip_id>/summary', TripSummaryView.as_view(), name='trip_summary'),
    path('<str:trip_id>/weather-md', TripWeatherView.as_view(), name='trip_weather'),
    path('<str:trip_id>/transport-md', TripTransportView.as_view(), name='trip_transport'),
    path('<str:trip_id>/hotel-md', TripHotelView.as_view(), name='trip_hotel'),
    path('<str:trip_id>/food-md', TripFoodView.as_view(), name='trip_food'),
    path('<str:trip_id>/itinerary-md', TripItineraryView.as_view(), name='trip_itinerary'),
    path('<str:trip_id>/budget-md', TripBudgetView.as_view(), name='trip_budget'),
    path('<str:trip_id>/status', TripStatusView.as_view(), name='trip_status'),
    path('<str:trip_id>/regenerate', RegenerateTripView.as_view(), name='regenerate_trip'),
    path('<str:trip_id>/delete', DeleteTripView.as_view(), name='delete_trip'),
    path('revise/<str:trip_id>', ReviseTripPlanView.as_view(), name='revise_trip'),  # 修订接口
    path('<str:trip_id>/download', DownloadTripView.as_view(), name='download_trip'),
]