import datetime
from django import forms 
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from catalog.models import Author,Genre

class RenewBookForm(forms.Form):
	renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
	
	def clean_renewal_date(self):
		data = self.cleaned_data['renewal_date']
		# import pdb;pdb.set_trace()

		# Check if a date is not in the past.
		if data < datetime.date.today():
			raise ValidationError(_('Invalid date - renewal in past'))

		# Check if a date is in the allowed range (+4 weeks from today).
		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))
		return data


class AuthorCreateForm(ModelForm):
	class Meta:
		model = Author
		fields = '__all__'
		labels = {'first_name':_('Enter the First Name')}
		help_text = {'first_name':_('First Name')}



class GenreCreateForm(ModelForm):
	class Meta:
		model = Genre
		fields= '__all__'


class AuthorDeleteForm(forms.Form):
	class Meta:
		model = Author
		fields =''
		



#of we can use model form as below 

# from django.forms import ModelForm

# from catalog.models import BookInstance

# class RenewBookModelForm(ModelForm):
#     class Meta:
#         model = BookInstance
#         fields = ['due_back']

# Note
# You can also include all fields in the form using fields = '__all__', or you can use exclude



# from django.forms import ModelForm

# from catalog.models import BookInstance

# class RenewBookModelForm(ModelForm):
#     def clean_due_back(self):
#        data = self.cleaned_data['due_back']

#        # Check if a date is not in the past.
#        if data < datetime.date.today():
#            raise ValidationError(_('Invalid date - renewal in past'))

#        # Check if a date is in the allowed range (+4 weeks from today).
#        if data > datetime.date.today() + datetime.timedelta(weeks=4):
#            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

#        # Remember to always return the cleaned data.
#        return data

#     class Meta:
#         model = BookInstance
#         fields = ['due_back']
#         labels = {'due_back': _('Renewal date')}
#         help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}

