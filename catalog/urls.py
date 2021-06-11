from django.conf.urls import url,include
from . import views
from catalog.views import BookListView, BookDetailView,AuthorListView,LoanedBooksByUserListView

from catalog.views import AllLoanedBooksByUserListView
from catalog.views import renew_book_librarian
from django.views.generic import RedirectView

app_name = 'catalog'

urlpatterns = [
    url(r'^$',views.index, name ='index'),
    url(r'^catalog/',RedirectView.as_view(pattern_name='catalog:index',permanent=True)),
    url(r'^books/',BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$',BookDetailView.as_view(), name ='book-detail'),
    url(r'^authors/',AuthorListView.as_view(),name='authors'),
    url(r'^mybooks/',LoanedBooksByUserListView.as_view(),name='my-borrowed'),
    url(r'^allborrowed/',AllLoanedBooksByUserListView.as_view(),name='all-borrowed'),
    url(r'^bookrenew/(?P<pk>\d+)$',views.renew_book_librarian,name='renew-book-librarian'),
]
