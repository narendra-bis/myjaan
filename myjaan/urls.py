"""myjaan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets 
from django.views.generic import RedirectView

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.

router = routers.DefaultRouter()
router.register(r'users',UserViewSet)



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'myapp/',include('myapp.urls')),
    url(r'',include('catalog.urls')),
    url(r'',include('console.urls')),
    url(r'accounts/',include('django.contrib.auth.urls')),
    # url(r'', include(router.urls)),
    # url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # url(r'',views.home),
    # url(r'', RedirectView.as_view(url='catalog/')),
]

# Use static() to add url mapping to serve static files during development (only)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
