
from django.urls import path
from django.conf.urls import url
from home import views


urlpatterns = [
	
	url(r'^$', views.index, name='home'),
    path('about', views.about, name='about')	
]