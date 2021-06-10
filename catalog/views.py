from django.shortcuts import render, redirect, reverse , get_object_or_404 
from django.http import HttpResponse
from catalog.models import Book, Author, BookInstance, Genre
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView



# Create your views here.


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
	queryset = Author.objects.all()[:5]
	template_name = "catalog/author_list.html"