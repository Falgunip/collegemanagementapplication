from rest_framework import serializers

from administrator.models import Studentapplication, Studentregistration


class StudentApplicationSerializer(serializers.ModelSerializer):
    """
      Created Student Application Serializer with all fields of Studentapplication model
    """
    class Meta:
        model = Studentapplication
        fields = '__all__'

class StudentRegistrationSerializer(serializers.ModelSerializer):
    """
      Created Student Registration Serializer with field profile pic of Studentregistration model
    """
    class Meta:
        model = Studentregistration
        # fields = ["father_name", "mobile_no"]
        fields = ["profile_pic"]