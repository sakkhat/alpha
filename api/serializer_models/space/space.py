from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ReadOnlyField

from space.models import Status


class SpaceStatusSerializer(ModelSerializer):
	space = ReadOnlyField(source='space.name')
	logo = ReadOnlyField(source='space.logo')
	class Meta:
		model = Status
		fields = [
			'total_favorite', 
			'total_pinned', 
			'rating', 
			'total_post',
			'logo',
			'space'
		]
