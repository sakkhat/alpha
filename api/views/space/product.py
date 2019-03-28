from api.serializer_models.space.product import ( ProductSerializer, ProductReactSerializer,
	ProductSerializerForReact)

from api.handler import activity
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

from space.models import Product, ProductReact



class PinnedProductListView(ListAPIView):
	serializer_class = ProductSerializer
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def get_queryset(self):
		request = self.request
		if not request.user.is_authenticated:
			raise NotFound('request not found')
		ac_id = self.kwargs['ac_id']
		if request.user.phone != ac_id:
			raise PermissionDenied('invalid request for this user')
		else:
			queryset = pinned_product_objects(request.user)
			return queryset



class ProductReactListView (ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = ProductReactSerializer

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
		raise NotFound('request not found')


class PinnedProductRequestView(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request, uid, format=None):
		req = request.GET.get('req', None)
		if req is not None:
			req = req.upper()
			res = activity.handle_pin(request.user, uid, req)
			if res:
				return Response({'response' : 'request accepted'});

		raise NotFound('request not found')