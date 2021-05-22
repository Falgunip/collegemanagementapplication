from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from administrator.models import MyUser, Department, Staffregistration


def register(request):
    """
     Rendering register html when user as a staff click on Staff Registration
    """
    return render(request,'staff/register.html')

def savestaff(request):
    """
     As MyUser is AbstractBase User, so for login authentication creating user with email and password.
     Retrieving department code
     Creating staff user with authenticated user,dept code, and other Staffregistration's  model fields
     Rendering main page to college management system
    """
    user = MyUser.objects.create_user(email=request.POST.get('email'), password=request.POST.get('password'))
    deptObj = Department.objects.get(code=request.POST.get('dept'))
    Staffregistration.objects.create(name=request.POST.get('name'), user=user, mobile_no=request.POST.get('mobile_no'), dept=deptObj,
                                     exp=request.POST.get('exp'),qualification=request.POST.get('qualification'),profile_pic=request.FILES['profile_pic'])
    return render(request, 'administrator/index.html',
                  {'message': "Congratulations !! You are successfully registered."})


def loginpage(request):
    """
     Rendering Staff login page when staff user clicks on Staff Login
    """
    return render(request, 'staff/login.html')

def dologin(request):
    """
     Authenticating of user with email and password on Login page
     if login successful then user redirects to the homepage
     if not successful then error message will show.
    """
    email=request.POST['email']
    password=request.POST['password']
    staff = authenticate(request, email=email, password=password)
    if staff is not None:
        login(request,staff)
        return HttpResponseRedirect('/staff/staffhome/')
    else:
        return render(request, 'staff/login.html', {'message': "Email and Password are not valid."})

@login_required(login_url='/staff/loginpage/')
def staffhome (request):
    """
     Rendering staff home page when staff user successfully logged in.
    """
    print(request.user.staffregistration)
    staff = request.user.staffregistration
    return render(request, 'staff/home.html', {'staff': staff})

@login_required(login_url='/staff/loginpage/')
def myprofile(request):
    """
     Rendering staff my profile page where logged in user related info is available.
    """
    staff = request.user.staffregistration
    return render(request, 'staff/myprofile.html',{'staff': staff})

@login_required(login_url='/student/loginpage/')
def staff_list_for_student(request):
    """
     Retrieving all objects of Staff Registration model
     Rendering staff list for student page where limited info is available of staff which student can see
    """
    stu = request.user.studentregistration
    staffobj = Staffregistration.objects.all()
    return render(request, 'staff/staff_list_for_student.html',{'student':stu,'staffs':staffobj})

@login_required(login_url='/staff/loginpage/')
def staff_all_detail(request):
    """
     Retrieving all objects of Staff Registration model
     Rendering staff all detail page where all the info is available of staff which any staff user can see
    """
    staff = request.user.staffregistration
    staffobj = Staffregistration.objects.all()
    return render(request, 'staff/staff_all_detail.html', {'staff': staff,'staffs': staffobj})

def stafflogout(request):
    """
     Logout function for staff user
    """
    logout(request)
    return HttpResponseRedirect('/staff/loginpage/')