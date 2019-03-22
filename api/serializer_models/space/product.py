from home.models import PinnedProduct

from rest_framework.serializers import ModelSerializer

from space.models import Product, ProductReact


class ProductSerializer(ModelSerializer):
	class Meta:
		model = Product
		fields = ('uid', 'title', 'price', 'logo_url','react_good', 'react_bad', 'react_fake')



class ProductReactSerializer(ModelSerializer):
	class Meta:
		model = ProductReact
		fields = ('__all__')



class ProductSerializerForReact(ModelSerializer):
	class Meta:
		model = Product
		fields = ('react_good', 'react_bad', 'react_fake')

