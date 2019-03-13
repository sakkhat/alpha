"""alpha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib.admin import site
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from home import views as index

from space.api.views import ProductListView

# from rest_framework import routers
# from space.views import PostViewSet



urlpatterns = [
	
	# managed all index functionality in home
    path('api/', include('generic.api_urls')), 
    path('', include('home.urls')),
    # path('admin/', site.urls),
    path('account/', include('account.urls')),
    path('space/', include('space.urls')),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
