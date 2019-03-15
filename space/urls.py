from django.urls import path

from space.views import manage,product
from space.api import views




urlpatterns = [
	path('create/', manage.create, name='space_create'),
	path('<name>/', manage.index, name='space_view'),

	path('product/create/', product.create, name='product_create'),
	path('product/<uid>/', product.manager, name='product_view'),
	
]