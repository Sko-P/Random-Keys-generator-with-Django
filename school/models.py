from django.db import models
from django.contrib.auth.models import User


# Create your models here.


#Physical activity not concerned
class Classroom(models.Model):


    pallier = models.IntegerField( null=True)
    typeclass = models.CharField(max_length=50, null=True)
    classr = models.IntegerField( null=True)
    president = models.ForeignKey('Teacher', null=True, on_delete=models.SET_NULL) #Doesn't delete the customer from database
    supervisor = models.ForeignKey('Supervisor', null= True, on_delete=models.SET_NULL )
    def __str__(self):
        return str(self.pallier)+self.typeclass+str(self.classr)


class Teacher(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    family_name= models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    classr = models.ManyToManyField('Classroom')

    def __str__(self):
        return self.family_name+" "+self.name




class Student(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    family_name= models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL)
    profile_pic = models.ImageField(default="user_profile2.png",null=True, blank=True)
    phone = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    final_mark = models.FloatField(null = True, blank=True)
    marks = models.ForeignKey('Mark',null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(null = True, blank=True)

    def __str__(self):
        return self.family_name+" "+self.name



class Supervisor(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    family_name= models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)

    


    def __str__(self):
        return self.family_name+" "+self.name


class Mark(models.Model):
    science = models.FloatField(null=True, blank=True)
    math = models.FloatField(null=True, blank=True)
    physics = models.FloatField(null=True, blank=True)
    arabic = models.FloatField(null=True, blank=True)
    french = models.FloatField(null=True, blank=True)
    english = models.FloatField(null=True, blank=True)
    ei = models.FloatField(null=True, blank=True)
    ep = models.FloatField(null=True, blank=True)
    ec = models.FloatField(null=True, blank=True)
