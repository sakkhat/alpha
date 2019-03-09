from rest_framework.generics import RetrieveAPIView, ListAPIView

from space.models import Product
from space.api.serializer import ProductAPI,ProductListAPI

class ProductView(RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductAPI



class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductListAPI
