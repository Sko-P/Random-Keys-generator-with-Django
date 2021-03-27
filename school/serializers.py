from rest_framework import serializers
from .models import *

"""
class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length= 100)
    email = serializers.EmailField(max_length=100)
    date = serializers.DateTimeField()


    #create method

    def create(self, validated_data): #When saving after object creation (a.save()) this function is being called
        return Article.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.title= validated_data.get('title', instance.title)
        instance.author= validated_data.get('author', instance.author)
        instance.email= validated_data.get('email', instance.email)
        instance.date = validated_data.get('data', instance.date)
        
        instance.save()
        return instance
"""

class ArticleSerializer(serializers.ModelSerializer): #A better visual than the first one
    class Meta:
        model = Article
        fields = ['id', 'title', 'author']