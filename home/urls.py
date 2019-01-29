
from django.urls import path
from django.conf.urls import url
from home import views


urlpatterns = [
	
	url(r'^$', views.index, name='home'),
    path('about', views.about, name='about'),
    path('auth', views.auth, name='auth'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('createpost', views.createpost, name='createpost')
]