from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken


from .serializers import ClassroomSerializer, StudentSerializer

#
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt #In case no possible integration of the csrf token

from .models import *

from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.

def mainpage(request):

    return render(request, "school/main.html")

@unauthenticated_user
def loginpage(request):

    if(request.user.is_authenticated):
        return redirect('rooms')
    else:

        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if(user is not None):
                login(request, user)
                group = request.user.groups.all()[0].name
                
                if(group == "teachers" or group == "supervisors" or group == "leaders"):
                    
                    return redirect('rooms')

                else:
                   
                    return redirect('classroom', pk=request.user.student.classroom.id)

            else:
                messages.info(request,"Username or password is incorrect")

        context = {}

        return render(request, 'school/login.html', context)

"""
Supervisor are allowed to see the classrooms they are concerned by
teacher are allowed to see the classrooms they teach
leaders are allowed to see all classroom
students are allowed to see their classroom only
"""

    
@login_required(login_url='login')
@allowed_users(["teachers", "supervisors", "leaders"])
def showclassrooms(request):
    group = request.user.groups.all()[0].name
    classrooms = ""
    if(group == "teachers"): #their classes
        # VERY IMPORTANT : the 'classroom' in classroom_set references the classroom table the teacher is related to thourgh foreignkey
        #So there is a need to mention there the table you would to get the rows from
        classrooms = request.user.teacher.classroom_set.all() #classroom is written in lowercase for the query

    elif(group == "supervisors"):
        classrooms = request.user.supervisor.classroom_set.all() 
        
    else: #all the leader case
        classrooms = Classroom.objects.all()


    
    print(classrooms)

    context = {
        "classrooms" : classrooms
    }

    return render(request, "school/classrooms.html", context)

def logoutUser(request):

    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(["teachers", "supervisors", "leaders", "students"])
def showclassroom(request, pk):
    students = Student.objects.filter(classroom=pk) #.object is when you get one result back only (one to one). This case is many to many
    print(students)
    return render(request, "school/classroom.html", {"students" : students})


def showstudent(request, pk, name):

    print(pk,name)
    student = Student.objects.get(classroom = pk, name = name)
    print(student)
    


    return render(request, "school/student.html", {"student": student})

class Classrooms_GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all()

    lookup_field = 'pk'
    #No data when logging out
    
    authentication_classes = [SessionAuthentication, BasicAuthentication,
    TokenAuthentication] #Checks Sessionauth if there is, then basic
    permission_classes = [IsAuthenticated]
   
    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        else:
            return self.list(request)

   
    def post(self, request):
        return self.create(request) 
    
    
    def put(self, request, pk=None):
        return self.update(request, pk)
    
    def delete(self,request, pk=None):
        return self.destroy(request, pk)

class Students_GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    lookup_field = 'pk'
    #No data when logging out
   
    authentication_classes = [SessionAuthentication, BasicAuthentication,
    TokenAuthentication] #Checks Sessionauth if there is, then basic
    permission_classes = [IsAuthenticated]
   
    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        else:
            return self.list(request)

   
    def post(self, request):
        return self.create(request) 
    
    
    def put(self, request, pk=None):
        return self.update(request, pk)
    
    def delete(self,request, pk=None):
        return self.destroy(request, pk)




@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,)) # Or remove rest list from settings.py
def Classroom_list(request):

    if(request.method == 'GET'):
        Classrooms = Classroom.objects.all()
        serializer = ClassroomSerializer(Classrooms, many=True)
        return Response(serializer.data)
        #return JsonResponse(serializer.data, safe= False)

    elif(request.method == 'POST'):
        
        serializer = ClassroomSerializer(data=request.data)
        
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
            #return JSONResponse(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)