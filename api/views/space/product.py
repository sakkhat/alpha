from account.models import Account

from api.serializer_models.space.product import ( ProductSerializer, ProductReactSerializer,
	ProductSerializerForReact)
from api.serializer_models.home import PinnedProductDetailSerializer
from api.handler import activity

from django.core.exceptions import ObjectDoesNotExist

from home.models import PinnedProduct

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from space.models import Product, ProductReact, Category
from space.models import _PRODDUCT_CATEGORY_KEY_DIC as category_key



class ProductReactListView (ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = ProductReactSerializer

	def get_queryset(self):
		request = self.request
		if not request.user.is_authenticated:
			raise NotFound('invalid request')
		ac_id = self.kwargs['ac_id']
		if request.user.phone != ac_id:
			raise PermissionDenied('invalid request for this user')
		else:
			queryset = ProductReact.objects.filter(user_id=request.user.id).order_by('-unix_time')
			return queryset



class ProductViewForReact (APIView):

	def get(self, request, uid, format=None):

		what = request.GET.get('react')
		if what is not None:
			if request.user.is_authenticated:
				product = activity.handle_react(request.user, uid, what)
				if product is not None:
					serializer = ProductSerializerForReact(product)
					return Response(serializer.data)

		try:
			product = Product.objects.get(uid=uid)
			serializer = ProductSerializerForReact(product)
			return Response(serializer.data)
		except ObjectDoesNotExist as e:
			pass
		raise NotFound('invalid request')


class PinnedProductRequestView(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request, uid, format=None):
		req = request.GET.get('req', None)
		if req is not None:
			req = req.upper()
			res = activity.handle_pin(request.user, uid, req)
			if res:
				return Response({'response' : 'request accepted'});

		raise NotFound('invalid request')


@api_view(['GET'])
def manager(request, format=None):
	category = request.GET.get('category', None)
	query = request.GET.get('query', None)
	pinned_by = request.GET.get('pinned_by', None)

	if category is not None:
		try:
			key = category_key.get(category)
			category_obj = Category.objects.get(name__iexact=key)
			result = Product.objects.filter(category_id=category_obj.id)
			serializer = ProductSerializer(result, many=True)
			return Response(serializer.data)

		except ObjectDoesNotExist as e:
			pass

	elif query is not None:
		pass

	elif pinned_by is not None:
		try:
			user = Account.objects.get(id=pinned_by)
			if request.user.id != user.id:
				raise PermissionDenied('request is not accepted')
			result = PinnedProduct.objects.filter(user_id=user.id)
			serializer = PinnedProductDetailSerializer(result, many=True)
			return Response(serializer.data)

		except ObjectDoesNotExist as e:
			pass


	raise NotFound('invalid request')