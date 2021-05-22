from django import forms
from administrator.models import Studentapplication

class StudentApplicationForm(forms.ModelForm):
    """
      Creating Student Application Form with all fields from model Studentapplication
      using this form for functions application and studentapply in views.py file in student app
    """
    class Meta:
        model = Studentapplication
        fields = '__all__'