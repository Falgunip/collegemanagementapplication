from django.urls import path

from . import views

app_name = 'student'
urlpatterns = [
    path('', views.application, name='application'),
    path('studentapply',views.studentapply, name='student_apply'),
    path('register',views.register, name='register'),
    path('savestudent', views.savestudent, name='savestudent'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('dologin', views.dologin, name='dologin'),
    path('stuhome/', views.stuhome, name='stuhome'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('studetaillist', views.studetaillist, name='studetaillist'),
    path('studetaillistdeptwise/<str:dept_code>/',views.studetaillistdeptwise, name='studetaillistdeptwise'),
    path('stulogout/', views.stulogout, name='stulogout'),
]