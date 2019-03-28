from django.urls import path

from space.views import manage,product


urlpatterns = [

	path('product/all/', product.manager, name='product_manager'),
	path('product/create/', product.create, name='product_create'),
	path('product/<uid>/', product.view, name='product_view'),
	path('product/<uid>/update/', product.update, name='product_update'),
	path('product/<uid>/update/<media_id>/', product.update_product_media, name='product_media_update'),

	path('create/', manage.create, name='space_create'),
	path('all/', manage.manager, name='space_manager'),
	path('<name>/', manage.index, name='space_view'),
	path('<name>/update/', manage.update, name='space_update'),
	path('<name>/update/<uid>/', manage.update_space_banner, name='space_banner_update'),
	
]	