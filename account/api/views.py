from account.api.serializers import (UserProductReact, UserFavoriteSpace,
	UserPinnedProductInfo)

from home.models import Favorite,PinnedProduct

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied,NotFound

from space.models import ProductReact



class UserProductReactList(ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = UserProductReact


	def get_queryset(self):
		request = self.request
		if not request.user.is_authenticated:
			raise NotFound('request not found')
		ac_id = self.kwargs['ac_id']
		if request.user.phone != ac_id:
			raise PermissionDenied('invalid request for this user')
		else:
			queryset = ProductReact.objects.filter(user=request.user).order_by('-uid')
			return queryset



class UserFavoriteSpaceList(ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = UserFavoriteSpace

	def get_queryset(self):
		request = self.request
		if not request.user.is_authenticated:
			raise NotFound('request not found')
		ac_id = self.kwargs['ac_id']
		if request.user.phone != ac_id:
			raise PermissionDenied('invalid request for this user')
		else:
			queryset = Favorite.objects.filter(user=request.user).order_by('-uid')
			return queryset



class UserPinnedProductList(ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = UserPinnedProductInfo

	def get_queryset(self):
		request = self.request
		if not request.user.is_authenticated:
			raise NotFound('request not found')
		ac_id = self.kwargs['ac_id']
		if request.user.phone != ac_id:
			raise PermissionDenied('invalid request for this user')
		else:
			queryset = PinnedProduct.objects.filter(user=request.user).order_by('-uid')
			return queryset