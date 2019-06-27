from django.urls import path

from space.manage import views as manage
from space.product import views as product


urlpatterns = [
	# path('', manage.route, name='space_route'),

	# path('product/', product.route, name='product_route'),
	# path('product/all/', product.manager, name='product_manager'),
	# path('create/', manage.create, name='space_create'),
	# path('all/', manage.manager, name='space_manager'),
	
	path('<space_name>/', manage.index, name='space_view'),
	path('<space_name>/update/', manage.update, name='space_update'),

	path('<space_name>/product/create/', product.create, name='product-create'),
	path('<space_name>/product/<product_uid>/', product.view, name='product-view'),
	path('<space_name>/product/<product_uid>/update/', product.update, name='product-update'),
	path('<space_name>/product/<product_uid>/update/delete/', product.delete, name='product-delete'),
]