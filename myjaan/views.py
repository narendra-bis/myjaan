from django.shortcuts import render
from django.http import HttpResponse


def home(request):
	# text = "<h1>welcome to myjaan</h1>"
	return render(request,'test.html')
	# return HttpResponse(text)