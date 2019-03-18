from account.api.serializers import (UserProductReact, UserFavoriteSpace,
	UserPinnedProductInfo, UserAccountSerializer)
from account.models import Account

from django.core.exceptions import ObjectDoesNotExist

from generic.media import Image
from generic.variables import USER_THUMBNAIL_PATH
from generic.views import json_response

from home.models import Favorite,PinnedProduct

from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied,NotFound
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
			queryset = ProductReact.objects.filter(user=request.user).order_by('-unix_time')
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
			queryset = Favorite.objects.filter(user=request.user).order_by('-unix_time')
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
			queryset = PinnedProduct.objects.filter(user=request.user).order_by('-unix_time')
			return queryset




@api_view(['GET', 'POST', 'PUT'])
def user_thumbnail_update(request, ac_id):

	if not request.user.is_authenticated:
		return json_response(request, {}, 'invalid request')

	if request.user.phone != ac_id:
		return json_response(request, {}, 'invalid request')

	if request.method == 'PUT':
		try:
			file = request.body
			img_src = Image.load(raw=file)

			try:
				user = Account.objects.get(phone=ac_id)
				img_path = Image.save(USER_THUMBNAIL_PATH, img_src)

				Image.delete(user.thumbnail)
				
				print(img_path)

				user.thumbnail = img_path
				user.save()

				serializer = UserAccountSerializer(user)
				return Response(serializer.data)


			except ObjectDoesNotExist as e:
				print(e)

		except Exception as e:
			print(e)
	
	return json_response(request, {}, 'invalid request')