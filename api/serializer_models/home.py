from home.models import Favorite, PinnedProduct,Notification
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ReadOnlyField



class FavoriteSpaceSerializer(ModelSerializer):
	space = ReadOnlyField(source='space.name')
	display = ReadOnlyField(source='space.display_name') 
	class Meta:
		model = Favorite
		fields = ('time_date', 'space', 'display')



class PinnedProductSerializer(ModelSerializer):
	space = ReadOnlyField(source='product.space.name')
	title = ReadOnlyField(source='product.title')
	class Meta:
		model = PinnedProduct
		fields = ('time_date', 'product','title', 'space') 



class PinnedProductDetailSerializer(ModelSerializer):
	uid = ReadOnlyField(source='product.uid')
	title = ReadOnlyField(source='product.title')
	price = ReadOnlyField(source='product.price')
	logo_url = ReadOnlyField(source='product.logo_url')
	react_good = ReadOnlyField(source='product.react_good')
	react_bad = ReadOnlyField(source='product.react_bad')
	react_fake = ReadOnlyField(source='product.react_fake')

	class Meta:
		model = PinnedProduct
		fields = ('uid', 'title', 'price', 'logo_url','react_good', 'react_bad', 'react_fake')



class NotificationSerializer(ModelSerializer):
	class Meta:
		model = Notification
		fields = ('uid', 'time_date', 'label', 'title', 'message', 'seen', 'action')

