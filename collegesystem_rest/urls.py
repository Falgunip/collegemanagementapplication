from django.urls import path
from . import views

"""
Created urlpatterns for API View of Student application, Student registration and user """
urlpatterns = [
    path("studentapplications/", views.StudentApplicationAPIView.as_view(), name="studentapplications"),
    path("studentregistrations/", views.StudentRegistrationAPIView.as_view(), name="studentregistrations"),
    path("user/", views.UserApiView.as_view(), name="user"),
]

"""
Created urlpattern for View Set for Student Application"""
from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'studentapplication',views.StudentApplicationViewSet, basename='studentapplication'),

urlpatterns += router.urls