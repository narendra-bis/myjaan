from django.contrib import admin
from django.db import models
from myapp.models import Student, Teacher

admin.site.register(Student)
admin.site.register(Teacher)

# Register your models here.

