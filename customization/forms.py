# customization/forms.py
from django import forms
from .models import Workout

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['exercise', 'rep_count', 'time_limit_seconds']
        widgets = {
            'exercise': forms.Select(attrs={'class': 'form-control'}),
            'rep_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'time_limit_seconds': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(WorkoutForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = False  # Set all fields as optional