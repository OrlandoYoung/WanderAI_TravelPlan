from django.contrib import admin
from .models import (
    Trip, TripSummary, TripWeather, TripTransport,
    TripHotel, TripFood, TripItinerary, TripBudget
)

# 注册模型到admin
@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('trip_id', 'origin', 'destination', 'start_date', 'status')
    search_fields = ('trip_id', 'destination')

@admin.register(TripSummary)
class TripSummaryAdmin(admin.ModelAdmin):
    list_display = ('trip',)

@admin.register(TripWeather)
class TripWeatherAdmin(admin.ModelAdmin):
    list_display = ('trip',)

# 其他模型的admin注册（略，与TripWeatherAdmin类似）