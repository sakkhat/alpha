from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view


from space.models import Product,ProductReact
from space.api.serializer import ProductAPI,ProductListAPI

from django.shortcuts import HttpResponse

class ProductView(RetrieveAPIView):
	
	serializer_class = ProductAPI

	def get_queryset(self):
		uid = self.kwargs['pk']
		queryset = Product.objects.filter(uid = uid)
		return queryset


class ProductListView(ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = ProductListAPI

	def get_queryset(self):

		raise PermissionDenied(detail='Invalid User')
		queryset = ProductReact.objects.all()
		queryset = queryset.union(queryset, all=True)
		queryset = queryset.union(queryset, all=True)
		queryset = queryset.union(queryset, all=True)
		queryset = queryset.union(queryset, all=True)
		print('\n', self.request.user, '\n')
		return queryset



