from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from administrator.models import Department


def index(request):
    """
      Main page of college management system
    """
    return render(request, 'administrator/index.html')

@login_required(login_url='/staff/loginpage/')
def deptlist(request):
    """
      Created for staff app, rendering all department's objects
      using this staff can see which student is from which department
    """
    staff = request.user.staffregistration
    departments = Department.objects.all()
    return render(request, 'administrator/deptlist.html',{'staff': staff,'departments':departments})
