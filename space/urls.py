from django.urls import path

from space.manage import views as manage
from space.product import views as product


urlpatterns = [
	path('create/', manage.create, name='space-create'),
	path('<space_name>/', manage.index, name='space-view'),
	path('<space_name>/update/', manage.update, name='space-update'),

	path('<space_name>/product/create/', product.create, name='product-create'),
	path('<space_name>/product/<product_uid>/', product.view, name='product-view'),
	path('<space_name>/product/<product_uid>/update/', product.update, name='product-update'),
	path('<space_name>/product/<product_uid>/update/delete/', product.delete, name='product-delete'),
]