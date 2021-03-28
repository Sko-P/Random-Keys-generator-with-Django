from django.urls import path
from .views import *



urlpatterns = [
    #API

    path('classroomsapi/',Classrooms_GenericAPIView.as_view(), name="classroomsapi"),
    path('studentsapi/', Students_GenericAPIView.as_view(), name="studentsapi"),
    path('studentsapi/<str:pk>', Students_GenericAPIView.as_view(), name="studentsapi"),
    

    #Pages
    path('',mainpage,name="main"),
    path('classrooms/', showclassrooms,name="rooms"),
    path('classrooms/<int:pk>',showclassroom, name="classroom"),
    path('classrooms/<int:pk>/<str:name>', showstudent, name="student"),
    path('login/', loginpage, name="login"),
    path('logout/', logoutUser, name="logout")

] 



""" path('api', views.article_list, name="list"),
    path('apiview', views.ArticleAPIView.as_view(), name="apiview"),
    path('apigeneric/', views.GenericAPIView.as_view(), name="genericview"),
    path('apigeneric/<str:pk>', views.GenericAPIView.as_view(), name="genericview"),
    path('apiviewdetail/<str:pk>', views.ArticleDetailAPI.as_view(), name="apiviewdetail"),
    path('detail/<str:pk>', views.article_detail, name="detail"),
    path('getdata',views.GetData,name="getdata"),
    path('getdata/data', views.ChartData.as_view())
"""