from home.models import PinnedProduct

from rest_framework.serializers import ModelSerializer, ReadOnlyField

from space.models import Product, ProductReact


class ProductSerializer(ModelSerializer):
	space = ReadOnlyField(source='space.name')
	class Meta:
		model = Product
		fields = ('uid', 'title', 'space', 'price', 'logo_url','react_good', 'react_bad', 'react_fake')



class ProductReactSerializer(ModelSerializer):
	class Meta:
		model = ProductReact
		fields = ('__all__')



class ProductSerializerForReact(ModelSerializer):
	class Meta:
		model = Product
		fields = ('react_good', 'react_bad', 'react_fake')

