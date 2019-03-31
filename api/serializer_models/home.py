from home.models import Favorite, PinnedProduct,Notification
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ReadOnlyField



class FavoriteSpaceSerializer(ModelSerializer):
	space = ReadOnlyField(source='space.name')
	class Meta:
		model = Favorite
		fields = ('unix_time', 'space')



class PinnedProductSerializer(ModelSerializer):
	class Meta:
		model = PinnedProduct
		fields = ('uid', 'unix_time', 'product') 




class NotificationSerializer(ModelSerializer):
	class Meta:
		model = Notification
		fields = ('uid', 'unix_time', 'label', 'title', 'message', 'seen', 'action')

