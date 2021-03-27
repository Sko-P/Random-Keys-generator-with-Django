#Django REST FRAMEWORK

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


from .serializers import ArticleSerializer

#
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt #In case no possible integration of the csrf token

from .models import *

User = get_user_model()
# Create your views here.


#API




### GENERICS

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    #No data when logging out
    lookup_field = 'pk'
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

    

# CLASS BASED VIEWS IN DJANGO REST

@permission_classes((permissions.AllowAny,))
class ArticleAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    @csrf_exempt
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
            #return JSONResponse(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
@permission_classes((permissions.AllowAny,))
class ArticleDetailAPI(APIView):
    def get_object(self, pk):
        try :
            print(pk)
            article = Article.objects.get(pk=pk)
            return article
        except Article.DoesNotExist:
            return HttpResponse(status = status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
#######################

### REST Framework api_view() Decorator 
@csrf_exempt 
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,)) # Or remove rest list from settings.py
def article_list(request):

    if(request.method == 'GET'):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
        #return JsonResponse(serializer.data, safe= False)

    elif(request.method == 'POST'):
        
        serializer = ArticleSerializer(data=request.data)
        
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
            #return JSONResponse(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def article_detail(request, pk):
    try :
        print(pk)
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT': #update
        
        serializer = ArticleSerializer(article, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
########################     
def GetData(request):
    chart = []
    emplacement = ["maison", "cuisine","salon","SB","chambre"]
    for i in range(0,5):
        chart.append({emplacement[i]:i})

    return JsonResponse(chart, safe=False)

#@requires_csrf_token
@csrf_exempt
def Showchart(request):
    
    return render(request, "chart/main.html")


class ChartData(APIView):
    #The two following lines are mandatory
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        chart = []
        emplacement = ["maison", "cuisine","salon","SB","chambre"]
        for i in range(0,5):
            if(i == 3):
                chart.append(45)
            else:
                chart.append(i)

        data = {
            "x" : chart,
            "y" : emplacement,
            
        }
        return Response(data)

    
    def post(self, request, format= None):
        serializer = ArticleSerializer(data=request.data)
        
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
            #return JSONResponse(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)