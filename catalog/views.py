
import datetime 
from django.shortcuts import render, redirect, reverse , get_object_or_404 
from django.http import HttpResponse
from catalog.models import Book, Author, BookInstance, Genre
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.forms import RenewBookForm, AuthorCreateForm
from django.http import HttpResponseRedirect
from django.views.generic import CreateView


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
			return HttpResponseRedirect(reverse('catalog:authors'))
	else:
		form = AuthorCreateForm()
	return render(request,'catalog/author_create.html',{'form':form})