from django.conf.urls import url
from django.views.generic import RedirectView
from myapp import views

app_name = "myapp"

urlpatterns = [
    url(r'index',views.index, name='index'),
    # url(r'myapp',RedirectView.as_view(pattern_name='myapp:index')),
    url(r'pel',views.pelidrom , name='pels'),
    url(r'prime',views.primeno, name='prime'),
    url(r'fibo',views.fibonacci,name='fibon'),
    url(r'leap',views.leapyear, name='leapyr'),
    url(r'rev',views.revers, name='revs'),
    url(r'art/(\d+)/',views.article, name='art')

    
]
