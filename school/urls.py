from django.urls import path
from .views import *



urlpatterns = [
    path('classrooms/', showclassrooms,name="rooms"),


] 



""" path('api', views.article_list, name="list"),
    path('apiview', views.ArticleAPIView.as_view(), name="apiview"),
    path('apigeneric/', views.GenericAPIView.as_view(), name="genericview"),
    path('apigeneric/<str:pk>', views.GenericAPIView.as_view(), name="genericview"),
    path('apiviewdetail/<str:pk>', views.ArticleDetailAPI.as_view(), name="apiviewdetail"),
    path('detail/<str:pk>', views.article_detail, name="detail"),
    path('getdata',views.GetData,name="getdata") ,
    path('getdata/data', views.ChartData.as_view())
"""