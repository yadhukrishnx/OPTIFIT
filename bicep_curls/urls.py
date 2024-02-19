from django.urls import path,include
from .views import index, video_feed, workoutcomplete, routinecomplete


urlpatterns = [
    path('', index, name='bicep_curls_index'),
    path('video_feed/', video_feed, name='bicep_curls_video_feed'),
    path('workoutcomplete', workoutcomplete, name='workoutcomplete'),
    path('routinecomplete', routinecomplete, name='routinecomplete')
]
