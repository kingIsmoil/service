from django import forms
from .models import Problem, Application

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'category']
        
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message', 'proposed_price']