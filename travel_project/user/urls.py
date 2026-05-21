from django.urls import path
from .views import (
    UserSavedTripsView, SaveTripView, UnsaveTripView,
    UserTripHistoryView
)

urlpatterns = [
    path('saved-trips/<str:user_id>/', UserSavedTripsView.as_view(), name='user_saved_trips'),
    path('save-trip', SaveTripView.as_view(), name='save_trip'),
    path('unsave-trip', UnsaveTripView.as_view(), name='unsave_trip'),
    path('trip-history', UserTripHistoryView.as_view(), name='user_trip_history'),
]