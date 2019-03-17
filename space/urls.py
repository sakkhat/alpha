from django.urls import path

from space.views import manage,product
from space.api import views




urlpatterns = [
	path('create/', manage.create, name='space_create'),
	path('<name>/', manage.index, name='space_view'),
	path('<name>/update/', manage.update, name='space_update'),
	path('<name>/update/<uid>/', manage.update_space_banner, name='space_banner_update'),

	path('product/create/', product.create, name='product_create'),
	path('product/<uid>/', product.manager, name='product_view'),
	path('product/<uid>/update/', product.update, name='product_update'),
	path('product/<uid>/update/<media_id>/', product.update_product_media, name='product_media_update'),
	
]