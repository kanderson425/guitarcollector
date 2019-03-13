from django.forms import ModelForm
from .models import Practice

class PracticeForm(ModelForm):
    class Meta:
        model = Practice
        fields = ['date', 'hour']