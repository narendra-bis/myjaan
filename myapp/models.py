from django.db import models

# Create your models here.

class Dreamreal(models.Model):
	website = models.CharField(max_length=50)
	mail = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	phonenumber = models.IntegerField()

	class Meta:
		db_table = "dreamreal"


class Test(models.Model):
	name = models.CharField(max_length=50)
	fname = models.CharField(max_length=50)

	class Meta:
		db_table = "mytest"



#common abstract class
class common(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	organisation = models.CharField(max_length=100)

	class Meta:
		abstract = True


class Student(common):
	name = models.CharField(max_length=100)
	roll_number = models.IntegerField(help_text="please use your roll number")
	place = models.CharField(max_length=100)


class Teacher(common):
	teacherid = models.CharField(max_length=50, help_text="use your id")
	username = models.CharField(max_length=50, help_text="please use username")



