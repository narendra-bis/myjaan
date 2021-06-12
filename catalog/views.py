
import datetime 
from django.shortcuts import render, redirect, reverse , get_object_or_404 
from django.http import HttpResponse
from catalog.models import Book, Author, BookInstance, Genre
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.forms import RenewBookForm, AuthorCreateForm, GenreCreateForm,AuthorDeleteForm
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.db.models import ProtectedError


# Create your views here.

@login_required
def index(request):
	"""view function for homepage of site"""
	# Generate counts of some of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	#book available
	num_instance_available = BookInstance.objects.filter(status__exact='a').count()

	num_authors = Author.objects.all().count()


	# Number of visits to this view, as counted in the session variable.
	num_visits = request.session.get('num_visits',0)
	request.session['num_visits'] = num_visits + 1


	# import pdb;pdb.set_trace()

	context ={
	'num_books':num_books,
	'num_instances':num_instances,
	'num_instance_available':num_instance_available,
	'num_authors':num_authors,
	'num_visits':num_visits
	}
	return render(request,'catalog/index.html',context=context)



#view for list of books
class BookListView(ListView):
	model = Book
	context_object_name = 'my_book_list'
	# queryset = Book.objects.filter(title__icontains='Hin')[:5] # Get 5 books containing the title Hin
	queryset = Book.objects.all()[:5]
	template_name = 'catalog/book_list.html'
	# def get_queryset(self):
	# 	return Book.objects.all()[:5]

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get the context
		context = super(BookListView, self).get_context_data(**kwargs)
		# Create any data and add it to the context
		context['test_some_data'] = 'This is just some data test'
		return context


# def book_detail_view(request, primary_key):
#     try:
#         book = Book.objects.get(pk=primary_key)
#     except Book.DoesNotExist:
#         raise Http404('Book does not exist')

#     return render(request, 'catalog/book_detail.html', context={'book': book})

# or 
# def book_detail_view(request, primary_key):
# 	book = get_object_or_404(Book, pk=primary_key)
#     return render(request, 'catalog/book_detail.html', context={'book': book})


class BookDetailView(DetailView):
	def get(self, request, *args, **kwargs):
		book = get_object_or_404(Book, pk=kwargs['pk'])
		context = {'book': book}
		return render(request, 'catalog/book_detail.html', context)


class AuthorListView(ListView):
	model = Author
	context_object_name = 'author_list'
	queryset = Author.objects.all()[:20]
	template_name = "catalog/author_list.html"

class GenreListView(ListView):
	model = Genre
	context_object_name = 'genre_list'
	queryset = Genre.objects.all()[:20]
	template_name = 'catalog/genre_list.html'

	

"""
function for borrowed books individual
"""
# @permission_required('catalog.can_mark_returned')
class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
	"""Generic class-based view listing books on loan to current user."""
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10
	# import pdb;pdb.set_trace()

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


	def get_context_data(self, **kwargs):
		# Call the base implementation first to get the context
		context = super(LoanedBooksByUserListView, self).get_context_data(**kwargs)
		# Create any data and add it to the context
		context['alluser'] = BookInstance.objects.filter(status__exact='o').order_by('due_back')
		return context



"""
function for all borrowed books
"""
class AllLoanedBooksByUserListView(LoginRequiredMixin, ListView):
	"""Generic class-based view listing books on loan to current user."""
	model = BookInstance
	template_name = 'catalog/allbookinstance_list_borrowed_user.html'
	paginate_by = 10
	# import pdb;pdb.set_trace()

	def get_queryset(self):
		return BookInstance.objects.filter(status__exact='o').order_by('due_back')




def renew_book_librarian(request, pk):
	book_instance = get_object_or_404(BookInstance, pk=pk)

	# If this is a POST request then process the Form data
	if request.method == "POST":
		# Create a form instance and populate it with data from the request (binding):
		form = RenewBookForm(request.POST)
		if form.is_valid():
			book_instance.due_back = form.cleaned_data['renewal_date']
			book_instance.save()
			messages.success(request,_("Book renewed successfully"))
			return HttpResponseRedirect(reverse('catalog:all-borrowed'))

	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})
	
	context = {
		'form': form,
		'book_instance':book_instance 

	}
	return render(request,'catalog/book_renew_librarian.html',context)


# class AuthorCreate(CreateView):
# 	model = Author
# 	form_class = AuthorCreateForm
# 	template_name = "catalog/author_create.html"


def create_author(request):
	if request.method=="POST":
		form = AuthorCreateForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,_('Auther created successfully'))
			return HttpResponseRedirect(reverse('catalog:authors'))
	else:
		form = AuthorCreateForm()
	return render(request,'catalog/author_create.html',{'form':form})


def create_genre(request):
	if request.method=='POST':
		form = GenreCreateForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,_('Genre created successfully'))
			return HttpResponseRedirect(reverse('catalog:genres-ls'))
	else:
		form = GenreCreateForm()
	return render(request,'catalog/genre_create.html',{'form':form})


"""
Function for update the author
"""
def update_author(request,pk):
	author_instance = get_object_or_404(Author,pk=pk)
	if request.method=="POST":
		form =AuthorCreateForm(request.POST)
		if form.is_valid():
			author_instance.first_name=form.cleaned_data['first_name']
			author_instance.last_name=form.cleaned_data['last_name']
			author_instance.date_of_birth=form.cleaned_data['date_of_birth']
			author_instance.date_of_death=form.cleaned_data['date_of_death']
			author_instance.save()
			messages.success(request,_('Updated Successfully'))
			return HttpResponseRedirect(reverse('catalog:authors'))
	else:
		context ={			
			'form':AuthorCreateForm(instance = author_instance)
		}	
	return render(request,'catalog/update_author.html', context)


"""
Function for Delete author
"""
def delete_author(request,pk):
	author_instance = get_object_or_404(Author,pk=pk)
	if request.method =='POST':
		if request.POST.get('yes_delete'):
			try:
				author_instance.delete()
				messages.success(request,_('Author deleted successfully'))
				return HttpResponseRedirect(reverse('catalog:authors'))
			except ProtectedError:
				messages.warning(request,_('Author is associated with book and can not be deleted'))
				return HttpResponseRedirect(reverse('catalog:authors'))
		else:
			return HttpResponseRedirect(reverse('catalog:authors'))	
	else:
		form = AuthorDeleteForm()
	return render(request,'catalog/author_confirm_delete.html',{'form':form})
