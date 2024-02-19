from django.db import models

from django.contrib.auth import get_user_model

class Workout(models.Model):
    EXERCISE_CHOICES = [
        ('squats', 'Squats'),
        ('bicep_curls', 'Bicep Curls'),
        # Add more exercise choices as needed
    ]

    routine = models.ForeignKey('Routine', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    exercise = models.CharField(max_length=20, choices=EXERCISE_CHOICES)
    rep_count = models.IntegerField()
    time_limit_seconds = models.IntegerField()

    def __str__(self):
        return f'{self.get_exercise_display()} - Reps: {self.rep_count}, Time: {self.time_limit_seconds}s'


class Routine(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Routine #{self.id} - User: {self.user.email}'
    
class WorkoutSettings(models.Model):
    exercise_name = models.CharField(max_length=100, default='Default Exercise Name')
    rep_count = models.IntegerField(default=0)
    time_limit = models.IntegerField(default=0)

    def __str__(self):
        return self.exercise_name

