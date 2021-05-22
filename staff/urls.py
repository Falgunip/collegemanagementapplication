from django.urls import path

from . import views

app_name = 'staff'
urlpatterns = [
   path('', views.register, name='register'),
   path('savestaff', views.savestaff, name='savestaff'),
   path('loginpage/', views.loginpage, name='loginpage'),
   path('dologin', views.dologin, name='dologin'),
   path('staffhome/', views.staffhome, name='staffhome'),
   path('myprofile/', views.myprofile, name='myprofile'),
   path('staff_list_for_student', views.staff_list_for_student, name='staff_list_for_student'),
   path('staff_all_detail',views.staff_all_detail,name='staff_all_detail'),
   path('stafflogout', views.stafflogout, name='stafflogout'),
]