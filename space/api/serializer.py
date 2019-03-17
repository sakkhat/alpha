from rest_framework import serializers

from space.models import Banner


class BannerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Banner
		fields = ('__all__')