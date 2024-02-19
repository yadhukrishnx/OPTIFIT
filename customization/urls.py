

# customization/urls.py
from django.urls import path
from registration import urls
from .views import customize_routine_view, workout_redirect_view, workout_completion, routine_completion
from .views import workout_settings

urlpatterns = [
    path('customize-routine/', customize_routine_view, name='customize_routine'),
    path('workout_redirect/<str:exercise_name>/<int:rep_count>/<int:time_limit>/', workout_redirect_view, name='workout_redirect'),
    path('settings/', workout_settings, name='workout_settings'),
    path('workout-completion/', workout_completion, name='workout_completion'),
    path('routine-completion/', routine_completion, name='routine_completion')

]

