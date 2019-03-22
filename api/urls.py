from django.urls import path, include
from api.views import account, home
from api.views.space import space
from api.views.space import product


urlpatterns = [

	path('user/<ac_id>/product_react_list/', product.ProductReactListView.as_view(),	 
		name='api_user_product_react_list'),

	path('user/<ac_id>/favorite_space_list/', home.FavoriteSpaceListView.as_view(), 
		name='api_user_favorite_space_list'),

	path('user/<ac_id>/pinned_product_list/', home.PinnedProductListView.as_view(), 
		name='api_user_pinned_prodcut_list'),


	path('user/<ac_id>/thumbnail/', account.user_thumbnail_update, name='user-thumbnail-name'),

	path('user/<ac_id>/notification/', home.NotificationListView.as_view(), name='user-notification'),

	path('product/<uid>/activity/react/', product.ProductViewForReact.as_view(), name='react-view'),

	path('product/<uid>/activity/pin/', product.PinnedProductRequestView.as_view(), name='pin-view'),
	
	path('space/<name>/activity/favorite/', space.FavoriteRequestView.as_view(), name='favorite-view'),

]