from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from .forms import MyForm
from django.contrib import messages 


# Create your views here.


def index(request):
	return render(request,'myapp/index.html')

"""
Function to check pelidrom number
"""
def pelidrom(request):
	if request.method == 'POST':
		form = MyForm(request.POST)
		if form.is_valid():
			number = (form.cleaned_data['number'])
			try:
				num = int(number)
				temp = num
				rev = 0
				while(num > 0):
					dig = num % 10
					rev = rev*10 + dig
					num = num//10
				if temp==rev:
					msg = " is a pelidrom number "
					mess = "{} {}".format(temp,msg)
					messages.add_message(request,messages.INFO,mess)
					# messages.add_message(request, messages.INFO,'This is Pelidrom number')
					return redirect(reverse('myapp:pels'))
				else:
					
					msg = " is NOT a pelidrom number"
					mess = "{} {}".format(temp,msg)
					messages.add_message(request,messages.WARNING, mess)
					return redirect(reverse('myapp:pels'))
			except ValueError:
				string = str(number)
				if string == string[::-1]:
					msg = " is a pelidrom number "
					mess = "{} {}".format(string,msg)
					messages.add_message(request,messages.INFO,mess)
					return redirect(reverse('myapp:pels'))
				else:
					msg = " string is NOT a pelidrom number"
					mess = "{} {}".format(string,msg)
					messages.add_message(request,messages.WARNING, mess)
					return redirect(reverse('myapp:pels'))
	else:
		form = MyForm()
	messages.add_message(request,messages.INFO,'Check for Pelidrome')
	return render(request,'myapp/oops.html',{'form':form})



"""
function for prime number 
"""
def primeno(request):
	if request.method == "POST":
		form = MyForm(request.POST)
		if form.is_valid():
			try:
				num = form.cleaned_data['number']
				temp = int(num)
				# import pdb;pdb.set_trace()
				if temp > 1:
					tmp = temp//2
					con=0
					for i in range(2,tmp):						
						if temp % i == 0:
							con=1							
							messages.add_message(request,messages.INFO,"Number is NOT prime")
							return redirect(reverse('myapp:prime'))
							break
					if con==0:						
						messages.add_message(request,messages.INFO,"This is Prime number")
						return redirect(reverse('myapp:prime'))
													
			except ValueError:
				messages.add_message(request,messages.INFO,"Kindly provide integer value")
				return redirect(reverse('myapp:prime'))
	else:
		messages.add_message(request,messages.INFO,"Check for Prime Number ")
		form = MyForm()
	return render(request,'myapp/oops.html',{'form':form})



"""
function to get fibonacci series
"""
def Fibonacci(n):
    f0, f1 = 0, 1
    for _ in range(n):
        yield f0
        f0, f1 = f1, f0+f1

def fibonacci(request):
	if request.method == "POST":
		form = MyForm(request.POST)
		if form.is_valid():
			term =  int(form.cleaned_data['number'])
			
			fibs = list(Fibonacci(term))
			messages.add_message(request,messages.INFO,fibs)
			return redirect(reverse('myapp:fibon'))
				
	else:
		messages.add_message(request,messages.INFO,"Create Fibonacci series up to ")
		form = MyForm()
	return render(request,'myapp/oops.html',{'form':form})



"""
Function to check leap year  
"""

def leapyear(request):
	if request.method == "POST":
		form = MyForm(request.POST)
		if form.is_valid():
			year = int(form.cleaned_data['number'])

			if (year % 4)==0:
				if (year % 100)==0:
					if (year % 400)==0:
						yr = ("{0} is a leap year ".format(year))
						messages.add_message(request,messages.INFO,yr)
						return redirect(reverse('myapp:leapyr'))
					else:
						yr = ("{0} is Not a leap year".format(year))
						messages.add_message(request,messages.INFO,yr)
						return redirect(reverse('myapp:leapyr'))
				else:
					yr = ("{0} is a leap year".format(year))
					messages.add_message(request,messages.INFO,yr)
					return redirect(reverse('myapp:leapyr'))
			else:
				yr = ("{0} is Not a leap year".format(year))
				messages.add_message(request,messages.INFO,yr)
				return redirect(reverse('myapp:leapyr'))
	else:
		messages.add_message(request,messages.INFO,"Check leap year ")
		form = MyForm()
	return render(request,'myapp/oops.html',{'form':form})



def revers(request):
	if request.method == "POST":
		form = MyForm(request.POST)
		if form.is_valid():
			temp_num = int(form.cleaned_data['number'])
			rev = 0
			while (temp_num > 0):
				dig = temp_num % 10
				rev = rev*10+dig
				temp_num = temp_num // 10
			msg = "The reverese digit is : {0}".format(rev)
			messages.add_message(request, messages.INFO,msg)
			return redirect(reverse('myapp:revs'))		
	else:
		messages.add_message(request, messages.INFO, "Reverse the digits")
		form = MyForm()
	return render(request,'myapp/oops.html',{'form':form})		




def article(request,articleid):
	# import pdb;pdb.set_trace()
	txt = "Displaying article ", articleid

	return HttpResponse(txt)