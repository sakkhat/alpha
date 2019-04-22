from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ReadOnlyField

from space.models import Status


class SpaceStatusSerializer(ModelSerializer):
	space = ReadOnlyField(source='space.name')
	class Meta:
		model = Status
		fields = ['rating', 'total_post','space']
