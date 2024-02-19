# squats/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video_feed/', views.video_feed, name='video_feed'),  # Updated URL pattern
    path('workoutcomplete/', views.workoutcomplete, name='workout_complete'),  # Updated URL pattern
    path('routinecomplete/', views.routinecomplete, name='routine_complete'),  # Updated URL pattern
]