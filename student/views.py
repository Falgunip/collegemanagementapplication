from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from administrator.form import StudentApplicationForm
from administrator.models import Studentapplication, Studentregistration, MyUser, Department


def application(request):
    """
     Retrieving Student Application form with all fields and rendering
     Rendering Application Page for Student user from main page of college management system
     where Student application form is available
    """
    form = StudentApplicationForm()
    return render(request, 'student/application.html',{"form":form})

def studentapply(request):
    """
     If Student Application form is valid means Student user filling form with all the fields
     than form will save and student user redirect to main page of college management system
     otherwise on Application page form errors will show.
    """
    # Studentapplication.objects.create(name=request.POST.get('name'),email=request.POST.get('email'),ssc_marks=request.POST.get('ssc_marks'),internal_marks=request.POST.get('internal_marks'))
    if request.method =='POST':
        student_application_form = StudentApplicationForm(request.POST)
        if student_application_form.is_valid():
            student_application_form.save()
            return HttpResponseRedirect('/administrator')
        else:
            return render(request, 'student/application.html',{"error":student_application_form.errors, "form":StudentApplicationForm()})


def register(request):
    """
     Retrieving all objects of Student application and department and rendering
     Rendering on register page from main page of college management system
    """
    student = Studentapplication.objects.all()
    depts = Department.objects.all()
    return render(request, 'student/register.html',{'student':student, 'depts':depts})

def savestudent(request):
    """
     Retrieving email and checking student user approved by admin or not
     As MyUser is AbstractBase User, so for login authentication creating user with email and password.
     Retrieving department code
     Creating student user with authenticated user,dept code, and other Studentregistration's  model fields
     Rendering main page to college management system
    """
    student = Studentapplication.objects.get(email=request.POST.get('email'))
    if student.approved == False:
        messages.error(request, "Sorry, you are not approved by management so you can't do registration.")
        return HttpResponseRedirect('/student/register')
    else:
        user = MyUser.objects.create_user(email=request.POST.get('email'),password=request.POST.get('password'))
        deptObj = Department.objects.get(code=request.POST.get('dept'))
        Studentregistration.objects.create(studentApplication=student,father_name=request.POST.get('father_name'),mobile_no= request.POST.get('mobile_no'),
                                           dept=deptObj,profile_pic = request.FILES['profile_pic'],user=user)
        return render(request, 'administrator/index.html', {'message': "Congratulations !! You are successfully registered."})


def loginpage(request):
    """
         Rendering Student login page when staff user clicks on Staff Login
    """
    return render(request, 'student/login.html')

def dologin(request):
    """
         Authenticating of user with email and password on Login page
         if login successful then user redirects to the homepage
         if not successful then error message will show.
    """
    email = request.POST['email']
    password = request.POST['password']
    stu = authenticate(request, email=email, password=password)
    if stu is not None:
        login(request, stu)
        return HttpResponseRedirect('/student/stuhome/')
    else:
        return render(request, 'student/login.html', {'message': "Email and Password are not valid."})

@login_required(login_url='/student/loginpage/')
def stuhome(request):
    """
         Rendering student home page when student user successfully logged in.
    """
    print(request.user)
    print(request.user.studentregistration)
    print(request.user.studentregistration.dept)
    student = request.user.studentregistration
    return render(request, 'student/home.html',{'student':student})

@login_required(login_url='/student/loginpage/')
def myprofile(request):
    """
         Rendering student my profile page where logged in user related info is available.
    """
    student = request.user.studentregistration
    return render(request, 'student/myprofile.html',{'student':student})

@login_required(login_url='/student/loginpage/')
def studetaillist(request):
    """
    Retrieving student by applying filter department from student registration and rendering
    so only those students will display which have same department
    Rendering to student detail page
    """
    stu = request.user.studentregistration
    students = Studentregistration.objects.filter(dept=stu.dept)
    return render(request, 'student/student_detail.html',{'student':stu,'students':students})

@login_required(login_url='/staff/loginpage/')
def studetaillistdeptwise(request,dept_code):
    """
    Retrieving all students of Student registration
    Retrieving departments using dept code
    Checking if student's department code matches with department code then make a separate result
    and send it to with particular department wise on student detail list department wise page
    else send message that there is no student of this department
    """
    staff = request.user.staffregistration
    students = Studentregistration.objects.all()
    # print(student)
    dept = Department.objects.get(code=dept_code)
    result = []
    for s in students:
       if s.dept.code == dept_code:
          result.append(s)
    if result:
        return render(request, 'student/student_detaillist_departmentwise.html', {'staff': staff,'students': result, 'dept': dept})
    else:
        return render(request, 'student/student_detaillist_departmentwise.html',{'staff': staff, 'message': f"There are no students of {dept}", 'dept':dept})

def stulogout(request):
    """
         Logout function for student user with clearing and deleting session
    """
    request.session.clear()
    request.session.delete()
    logout(request)
    return HttpResponseRedirect("/student/loginpage/")