
from django.urls import path,include
from .views import view

urlpatterns = [
	path('', view.manager , name='view-manager'),
]