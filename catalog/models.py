import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from django.conf import settings

# Create your models here.


class Genre(models.Model):
	"""model representing a book genre"""
	name = models.CharField(max_length=100, help_text="Enter a book genre(e.g.Science Fiction, French Poetry etc.)")

	def __str__(self):
		return self.name


class Language(models.Model):
	"""Model representing a Language (e.g. English, French, Japanese, etc.)"""
	name = models.CharField(max_length=100, help_text="Enter the book's natural language (e.g. English, French, Japanese etc")

	def __str__(self):
		return self.name


"""
Model representing Author 
"""
class Author(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null=True, blank=True)
	date_of_death = models.DateField('died', null=True, blank=True)

	class Meta:
		ordering = ['last_name','first_name']

	# def get_absolute_url(self):
	# 	return reverse('author-detail', args=[str(self.id)])

	def __str__(self):		
		return '{} {}'.format(self.last_name, self.first_name)




"""
Model representing a book 
"""
class Book(models.Model):
	title = models.CharField(max_length=200)
	# Foreign Key used because book can only have one author, but authors can have multiple books
	author = models.ForeignKey(Author,on_delete=models.PROTECT, null=True)
	summary = models.TextField(max_length=1000, help_text="Enter the brief discription of the book")
	isbn = models.CharField('ISBN', max_length=13, unique=True,
		help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
	# ManyToManyField used because genre can contain many books. Books can cover many genres.
	genre = models.ManyToManyField(Genre, help_text="select a genre for this book")

	language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

	class Meta:
		ordering = ['title', 'author']

	def __str__(self):
		"""String for representing the Model object."""
		return self.title

	"""Returns the url to access a particular book instance."""
	def get_absolute_url(self):
		return reverse('catalog:book-detail', args=[str(self.id)])


	def display_genre(self):
		"""Create a string for the Genre. This is required to display genre in Admin."""
		return ','.join(genre.name for genre in self.genre.all()[:3])

	display_genre.short_description = 'Genre'



"""
Book instance
"""
class BookInstance(models.Model):
	"""Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
	pkid = models.CharField(max_length=100,primary_key=True)
	id = models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	book = models.ForeignKey(Book, on_delete=models.PROTECT, null=True)
	imprint = models.CharField(max_length=200)
	due_back =  models.DateField(null=True, blank=True)

	load_status = (
		('m','Maintanance'),
		('o','On loan'),
		('a','Available'),
		('r','reserved')

		)
	status = models.CharField(max_length=1, choices=load_status, blank=True, default='m', help_text="Book availibility")

	class Meta:
		ordering = ['due_back']
		permissions = (("can_mark_returned", "Set book as returned"),)
	
	def is_overdue(self):
		if self.due_back and date.today() > self.due_back :
			return True
		else:
			return False

	def __str__(self):
		return self.book.title






	


