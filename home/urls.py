
from django.urls import path,include
from .views import view

urlpatterns = [
	path('', view.index , name='index'),
]