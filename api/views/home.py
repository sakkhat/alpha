
from api.serializer_models.home import (NotificationSerializer,PinnedProductSerializer,
	FavoriteSpaceSerializer)

from generic.query import pinned_product_objects

from home.models import PinnedProduct, Notification, Favorite

from rest_framework.exceptions import PermissionDenied,NotFound
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


QUERY = 'SELECT home_favorite.uid, home_favorite.unix_time, space_space.name FROM home_favorite INNER JOIN space_space ON home_favorite.space_id=space_space.id WHERE home_favorite.user_id='

class NotificationListView(ListAPIView):
	serializer_class = NotificationSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		if not user.is_authenticated:
			raise NotFound('request not found')
		ac_id = self.kwargs['ac_id']
		if user.phone != ac_id:
			raise PermissionDenied('invalid request for this user')

		else:
			queryset = Notification.objects.filter(user=user).order_by('-uid')
			return queryset




class FavoriteSpaceListView (ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = FavoriteSpaceSerializer

	def get_queryset(self):
		request = self.request
		if not request.user.is_authenticated:
			raise NotFound('request not found')
		ac_id = self.kwargs['ac_id']
		if request.user.phone != ac_id:
			raise PermissionDenied('invalid request for this user')
		else:
			# queryset = Favorite.objects.filter(user=request.user).order_by('-unix_time')
			queryset = Favorite.objects.raw(QUERY+str(request.user.id))
			return queryset




class PinnedProductListView (ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = PinnedProductSerializer

	def get_queryset(self):
		request = self.request
		if not request.user.is_authenticated:
			raise NotFound('request not found')
		ac_id = self.kwargs['ac_id']
		if request.user.phone != ac_id:
			raise PermissionDenied('invalid request for this user')
		else:
			queryset = PinnedProduct.objects.filter(user=request.user).order_by('-unix_time')
			return queryset




