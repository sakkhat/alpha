from django.urls import path

from space.manage import views as manage
from space.product import views as product


urlpatterns = [
	path('', manage.route, name='space_route'),

	path('product/', product.route, name='product_route'),
	path('product/all/', product.manager, name='product_manager'),
	path('product/create/', product.create, name='product_create'),
	path('product/<uid>/', product.view, name='product_view'),
	path('product/<uid>/update/', product.update, name='product_update'),
	path('product/<uid>/update/delete/', product.delete, name='product_delete'),

	path('create/', manage.create, name='space_create'),
	path('all/', manage.manager, name='space_manager'),
	path('<name>/', manage.index, name='space_view'),
	path('<name>/update/', manage.update, name='space_update'),
]