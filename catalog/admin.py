from django.contrib import admin
from catalog.models import Book, Author, Genre, BookInstance,Language 
# Register your models here.


# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(BookInstance)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name','first_name','date_of_birth','date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
	# pass
# admin.site.register(Author, AuthorAdmin)



class BookInstanceInline(admin.TabularInline):
	model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title','author','display_genre')
	inlines = [BookInstanceInline]
	# pass
# admin.site.register(Book, BookAdmin)



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	pass
# admin.site.register(Genre, GenreAdmin)



@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
	pass



@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )
	
	# pass
# admin.site.register(BookInstance, BookInstanceAdmin)


