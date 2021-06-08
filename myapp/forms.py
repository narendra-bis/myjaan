from django import forms

class MyForm(forms.Form):
	number = forms.CharField(max_length=100, label='Enter the number ')