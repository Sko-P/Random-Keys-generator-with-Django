from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Teacher)
admin.site.register(Classroom)
admin.site.register(Student)
admin.site.register(Supervisor)
admin.site.register(Mark)