from space.models import Product, Account
from rest_framework import serializers

class PostSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Product
		fields = ('price', 'description')


class AccountSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Account
		fields = ('id_name', 'display_name', 'phone')