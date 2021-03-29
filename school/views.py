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
@login_required(login_url='login')
def mainpage(request):

    return render(request, "school/main.html")

@unauthenticated_user
def loginpage(request):

    if(request.user.is_authenticated):
        return redirect('classrooms')
    else:
        
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if(user is not None):
                login(request, user)
                group = request.user.groups.all()[0].name
                
                if(group == "teachers" or group == "supervisors" or group == "leaders"):
                    
                    return redirect('classrooms')

                else:
                   
                    return redirect('classroom', pk=request.user.student.classroom.id)

            else:
                messages.info(request,"Username or password is incorrect")

        context = {}

        return render(request, 'school/login.html', context)



def logoutUser(request):

    logout(request)
    return redirect('login')


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
        classrooms = request.user.teacher.classr.all()
    elif(group == "supervisors"):
        classrooms = request.user.supervisor.classroom_set.all() #This is correct because the supervisor hasn't a Classroom field
        print(classrooms)
    else: #all the leader case
        classrooms = Classroom.objects.all()


    
    print(classrooms)

    context = {
        "classrooms" : classrooms
    }

    return render(request, "school/classrooms.html", context)


@login_required(login_url='login')
@allowed_users(["teachers", "supervisors", "leaders", "students"])
def showclassroom(request, pk):
    """
    print(request.user.student)
    print(Student.objects.filter(classroom=pk))
    print(request.user.student not in Student.objects.filter(classroom=pk))
    print(request.user.student.classroom.id)
    """
    if(request.user.groups.all()[0].name == "students"):
       
        if(request.user.student not in Student.objects.filter(classroom=pk)):
            return redirect('classroom', pk=request.user.student.classroom.id)
    elif(request.user.groups.all()[0].name == "teachers"):
        classrooms = request.user.teacher.classr.all()
        print("Teacher", classrooms)
        if(Classroom.objects.get(id=pk) not in classrooms):
            
            return redirect('classrooms')

    students = Student.objects.filter(classroom=pk) #.object is when you get one result back only (one to one). This case is many to many
    #print(students)
    return render(request, "school/classroom.html", {"students" : students})

@login_required(login_url='login')
@allowed_users(["teachers", "supervisors", "leaders", "students"])
def showstudent(request, pk, name):

    print(pk,name)
    student = Student.objects.get(classroom = pk, name = name)
    print(student)
    
   
    #print(Mark._meta.fields[0].name)

    note_object = student.marks

    names = []
    for i in Mark._meta.fields:
        if(i.name != "id"):
            names.append(i.name)

    field_value = []
    for i in names:
        field_value.append(getattr(note_object, i))

    print(field_value)

    global_score = 0

    for i in field_value:
        global_score += i

    global_score /= len(field_value)
    print(global_score)

    context = {
        "student": student,
        "fieldnames" : names,
        'fieldvalues' : field_value,
        'global_score' : global_score
        
        }
    return render(request, "school/student.html", context)

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