from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
# Create your views here.
from administrator.models import Studentapplication, Studentregistration, MyUser, Department
from rest_framework.response import Response

from collegesystem_rest.serializer import StudentApplicationSerializer, StudentRegistrationSerializer


class StudentApplicationAPIView(APIView):
    """
       Requires token authentication
       Only authenticated users are able to access this view
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
          Retrive list of students applications which have approved=True.
        """
        student_applications = Studentapplication.objects.filter(approved=True)
        ser_obj_studentapplication = StudentApplicationSerializer(student_applications, many=True)
        return Response(ser_obj_studentapplication.data)

        # student_applications = Studentapplication.objects.all()
        # ser_obj_studentapplication = StudentApplicationSerializer(student_applications, many=True)
        # return Response(ser_obj_studentapplication.data)

    def put(self, request, format=None):
        """
          Update student data
        """
        if not request.data.get("stu_id") or not request.data.get("name"):
            return Response({"message": "Not a valid request"}, status=status.HTTP_400_BAD_REQUEST)
        stu_id = request.data["stu_id"]
        name = request.data["name"]
        sscmarks = request.data["sscmarks"]
        stu_app_obj = Studentapplication.objects.get(id=stu_id)
        stu_app_obj.name = name
        stu_app_obj.ssc_marks = sscmarks
        stu_app_obj.save()
        return Response({"message": "Successfully Updated"})

    def post(self, request, format=None):
        """
          Insert or create new student data
        """
        serialize_obj = StudentApplicationSerializer(data=request.data)
        if serialize_obj.is_valid():
            serialize_obj.save()
            return Response(serialize_obj.data, status=status.HTTP_201_CREATED)
        return Response(serialize_obj.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
          Delete student data
        """
        stu_id = request.data["stu_id"]
        student_application = Studentapplication.objects.get(id=stu_id)
        student_application.delete()
        return Response({"message": "Successfully Deleted"}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, format=None):
        """
          Partially update student data
        """
        student_application = Studentapplication.objects.get(id=request.data["stu_id"])
        serialize_obj = StudentApplicationSerializer(student_application, data=request.data, partial=True)
        if serialize_obj.is_valid():
            serialize_obj.save()
            return Response(serialize_obj.data, status=status.HTTP_201_CREATED)
        return Response(serialize_obj.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentRegistrationAPIView(APIView):
    def get(self, request, format=None):
        """
          Retrive list of all students.
        """
        student_registrations = Studentregistration.objects.all()
        ser_obj_studentregistration = StudentRegistrationSerializer(student_registrations, many=True)
        return Response(ser_obj_studentregistration.data)

    def put(self, request, format=None):
        """
          Update student data from Student Registration
        """
        if not request.data.get("stu_id"):
            return Response({"message": "Not a valid request"}, status=status.HTTP_400_BAD_REQUEST)
        stu_id = request.data["stu_id"]
        dept = request.data["dept"]
        stu_reg_obj = Studentregistration.objects.get(id=stu_id)
        stu_reg_obj.dept = dept
        stu_reg_obj.save()
        return Response({"message":"Successfully Updated"})

    # def post(self,request,format=None):
    #     """
    #      Insert or create new student data
    #      """
    #     serialize_obj = StudentRegistrationSerializer(data=request.data)
    #     application = Studentapplication.objects.get(email=request.data.get("email"))
    #     user = MyUser.objects.create_user(email=request.data.get("email"), password=request.data.get("password"))
    #     dept = Department.objects.get(code=request.POST.get('dept'))
    #     if serialize_obj.is_valid():
    #         serialize_obj.save(studentApplication=application, user=user, dept=dept)
    #         return Response(serialize_obj.data, status=status.HTTP_201_CREATED)
    #     return Response(serialize_obj.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
     """
      Insert or create new student data
      """
     serialize_obj = StudentRegistrationSerializer(data=request.data)
     if serialize_obj.is_valid():
        serialize_obj.save()
        return Response(serialize_obj.data, status=status.HTTP_201_CREATED)
     return Response(serialize_obj.errors, status=status.HTTP_400_BAD_REQUEST)


class UserApiView(APIView):
    """
      Checking credentials with token
    """
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"message": "Invalid Credentials"})

    def delete(self, request):
        """
         Deleting token to cancel user's authentication
        """
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        Token.objects.get(user=user).delete()
        return Response({"message": "Successfully Deleted"}, status=status.HTTP_204_NO_CONTENT)

class StudentApplicationViewSet(viewsets.ViewSet):
    """
      Testing different methods with View Sets
    """
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    @action(methods=["GET"], detail=False)
    def get_students(self, request):
        """
          Retrieving all students from Student application
        """
        students = list(Studentapplication.objects.values())
        return Response(students)

    @action(methods=["GET"],detail=False)
    def get_students_by_approved(self, request):
        """
          Retrieving all students from Student application with applying filter Approved value True
        """
        students = list(Studentapplication.objects.filter(approved=request.data.get("approved")).values("id","name","email","approved"))
        return Response(students)

    @action(methods=["GET", "POST"], detail=False)
    def students_by_id(self, request):
        """
          GET - Retrieving all students from Student application with applying filter id
          POST - Creating new student using Student application serializer
        """
        if request.method == "GET":
            students = Studentapplication.objects.filter(id=request.data.get("id")).values("id", "name", "email",)
            return Response(students)
        elif request.method == "POST":
            serialize_obj = StudentApplicationSerializer(data=request.data)
            if serialize_obj.is_valid():
                serialize_obj.save()
                return Response(serialize_obj.data, status=status.HTTP_201_CREATED)
            return Response(serialize_obj.errors, status=status.HTTP_400_BAD_REQUEST)












