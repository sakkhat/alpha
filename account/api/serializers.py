from account.models import Account

from home.models import Favorite, PinnedProduct

from rest_framework import serializers as rest_serializer

from space.models import ProductReact

class UserProductReact(rest_serializer.ModelSerializer):
	class Meta:
		model = ProductReact
		fields = ('__all__')


class UserFavoriteSpace(rest_serializer.ModelSerializer):
	class Meta:
		model = Favorite
		fields = ('uid', 'unix_time', 'space')


class UserPinnedProductInfo(rest_serializer.ModelSerializer):
	class Meta:
		model = PinnedProduct
		fields = ('uid', 'unix_time', 'product') 


class UserAccountSerializer(rest_serializer.ModelSerializer):
	class Meta:
		model = Account
		fields = ('thumbnail',)
